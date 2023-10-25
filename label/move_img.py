#复制和移动指定后缀名文件
import os
import shutil


def copy_images(source_folder, destination_folder):
    # 创建目标文件夹（如果不存在）
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    total_images = 0


    # 遍历源文件夹中的所有文件和子文件夹
    for root, _, files in os.walk(source_folder):
        for filename in files:
            source_path = os.path.join(root, filename)

            # 检查文件是否为图片（这里假设只处理常见的图片格式）
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                destination_path = os.path.join(destination_folder, filename)

                # 复制图片文件
                shutil.copy2(source_path, destination_path)
                total_images += 1
                print(f"复制 {filename} 到 {destination_path}")

    print(f"共复制 {total_images} 张图片")


def move_images(source_folder, destination_folder):
    # 创建目标文件夹（如果不存在）
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    total_images = 0

    # 遍历源文件夹中的所有文件和子文件夹
    for root, _, files in os.walk(source_folder):
        for filename in files:
            source_path = os.path.join(root, filename)

            # 检查文件是否为图片（这里假设只处理常见的图片格式）
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                destination_path = os.path.join(destination_folder, filename)

                # 剪切图片文件
                shutil.move(source_path, destination_path)
                print(f"剪切 {filename} 到 {destination_path}")

                total_images += 1

    print(f"共剪切 {total_images} 张图片")


if __name__ == "__main__":
    source_folder = r"D:\ai-video\0927"
    destination_folder = r"D:\ai-video\0927pic"

    move_images(source_folder, destination_folder)

#藏文件