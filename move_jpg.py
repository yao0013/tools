#移动文件
import os
import shutil

def move_jpg_files(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    total_images = 0

    for root, _, files in os.walk(source_folder):
        for file in files:
            if file.lower().endswith(".xml"):
                source_path = os.path.join(root, file)
                destination_path = os.path.join(destination_folder, file)
                shutil.move(source_path, destination_path)
                print(f"Moved {file} to {destination_folder}")
                total_images += 1

    print(f"共移动 {total_images} 个文件")

if __name__ == "__main__":
    source_folder = r"D:\ai-video\2023-08-15"
    destination_folder = r"D:\ai-video\2023-08-15\xml"

    move_jpg_files(source_folder, destination_folder)