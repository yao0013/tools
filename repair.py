import os
import subprocess

def repair_videos(input_folder, output_folder):
    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".mp4"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # 使用MP4Box修复视频
            repair_command = ["MP4Box", "-add", input_path, output_path]
            subprocess.run(repair_command, capture_output=True)

            print(f"修复完成：{filename}")

# 指定输入和输出文件夹路径
input_folder = "/path/to/input/folder"
output_folder = "/path/to/output/folder"

# 调用修复函数
repair_videos(input_folder, output_folder)
