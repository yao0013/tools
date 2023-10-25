import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import shutil

class ImageViewer:
    def __init__(self, master):
        self.master = master
        self.image_paths = []
        self.current_index = 0
        self.destination_folders = {}

        self.master.title("Image Viewer")

        self.image_label = tk.Label(master)
        self.image_label.pack()

        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)

        self.previous_button = tk.Button(button_frame, text="Previous", command=self.show_previous_image)
        self.previous_button.pack(side="left")


        self.next_button = tk.Button(button_frame, text="Next", command=self.show_next_image)
        self.next_button.pack(side="right")

        with open("config.txt", "r") as config_file:
            button_count = int(config_file.read())

        # Create a dictionary to store buttons
        self.move_buttons = {}

        # Create buttons based on the button count
        for i in range(1, button_count + 1):
            folder_name = self.get_folder_name(i)  # Get folder name based on button number
            button_text = f"{i}. {folder_name}"

            # Dynamically create button variable names
            button_var_name = f"move_button_{i}"
            self.move_buttons[button_var_name] = tk.Button(button_frame, text=button_text,
                                                           command=lambda i=i: self.move_to_folder(i), width=20,
                                                           height=2)
            self.move_buttons[button_var_name].pack()

            root.bind(str(i), lambda event, i=i: self.move_to_folder(i))  # Remove invoke()

        # 设置快捷键事件绑定
        for i in range(1, button_count + 1):
            master.bind(str(i), lambda event, i=i: self.move_to_folder(i))

    def get_folder_name(self, folder_number):
        folder_name = self.destination_folders.get(folder_number)
        if not folder_name:
            folder_name = filedialog.askdirectory()
            self.destination_folders[folder_number] = folder_name
        return folder_name


        self.load_image_folder()


    def load_image_folder(self, folder_path=None):
        if folder_path is None:
            folder_path = filedialog.askdirectory()
        if folder_path:
            for root_dir, _, files in os.walk(folder_path):
                image_paths = [os.path.join(root_dir, file) for file in files if
                               file.endswith(('.jpg', '.jpeg', '.png'))]
                self.image_paths.extend(image_paths)

            if self.image_paths:
                self.current_index = 0
                self.display_image()

    def display_image(self):
        if 0 <= self.current_index < len(self.image_paths):
            image_path = self.image_paths[self.current_index]
            image = Image.open(image_path)
            image = image.resize((1280, 720))  # 调整图像大小
            photo = ImageTk.PhotoImage(image)

            self.image_label.configure(image=photo)
            self.image_label.image = photo

    def show_previous_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.display_image()
            self.next_button.config(state=tk.NORMAL)
        if self.current_index == 0:
            self.previous_button.config(state=tk.DISABLED)

    def show_next_image(self):
        if self.current_index < len(self.image_paths) - 1:
            self.current_index += 1
            self.display_image()
            self.previous_button.config(state=tk.NORMAL)

        if self.current_index == len(self.image_paths) - 1:
            self.next_button.config(state=tk.DISABLED)

    def move_to_folder(self, folder_number):
        if folder_number in self.destination_folders:
            selected_folder = self.destination_folders[folder_number]
            if selected_folder:
                image_path = self.image_paths[self.current_index]
                image_filename = os.path.basename(image_path)
                new_path = os.path.join(selected_folder, image_filename)
                base_name, extension = os.path.splitext(image_filename)
                counter = 1
                while os.path.exists(new_path):
                    new_filename = "{}_{}{}".format(base_name, counter, extension)
                    new_path = os.path.join(selected_folder, new_filename)
                    counter += 1
                shutil.move(image_path, new_path)
                self.image_paths.pop(self.current_index)
                if self.current_index >= len(self.image_paths):
                    self.current_index = max(0, len(self.image_paths) - 1)
                self.display_image()
        else:
            folder_path = filedialog.askdirectory()
            if folder_path:
                self.destination_folders[folder_number] = folder_path

root = tk.Tk()
app = ImageViewer(root)
root.mainloop()
