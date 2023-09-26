import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import shutil
import time

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

        previous_button = tk.Button(button_frame, text="Previous", command=self.show_previous_image)
        previous_button.pack(side="left")

        next_button = tk.Button(button_frame, text="Next", command=self.show_next_image)
        next_button.pack(side="right")

        move1_button = tk.Button(button_frame, text="1.没用", command=lambda: self.move_to_folder(1), width=20, height=2)
        move1_button.pack()
        root.bind("1", lambda event: move1_button.invoke())


        move2_button = tk.Button(button_frame, text="2.混合", command=lambda: self.move_to_folder(2), width=20, height=2)
        move2_button.pack()
        #设置快捷键
        root.bind("2", lambda event: move2_button.invoke())

        move3_button = tk.Button(button_frame, text="3.反光衣", command=lambda: self.move_to_folder(3), width=20, height=2)
        move3_button.pack()
        root.bind("3", lambda event: move3_button.invoke())


        move4_button = tk.Button(button_frame, text="4.普通", command=lambda: self.move_to_folder(4), width=20, height=2)
        move4_button.pack()
        root.bind("4", lambda event: move4_button.invoke())

        # 设置快捷键事件绑定
        master.bind("1", lambda event: self.move_to_folder(1))
        master.bind("2", lambda event: self.move_to_folder(2))
        master.bind("3", lambda event: self.move_to_folder(3))
        master.bind("4", lambda event: self.move_to_folder(4))

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

    def show_next_image(self):
        if self.current_index < len(self.image_paths) - 1:
            self.current_index += 1
            self.display_image()

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