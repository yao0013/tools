import os
import subprocess
from tqdm import tqdm

def convert_to_h264(input_path, output_path):
    command = [
        'ffmpeg',
        '-i', input_path,
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', 'experimental',
        '-b:a', '192k',
        output_path
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def convert_videos_in_directory(input_directory, output_directory):
    # 创建输出目录（如果不存在）
    os.makedirs(output_directory, exist_ok=True)

    # 获取所有视频文件
    video_files = []
    for root, _, files in os.walk(input_directory):
        for file in files:
            if file.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
                video_files.append(os.path.join(root, file))

    # 处理视频文件并显示进度条
    for video_file in tqdm(video_files, desc='Converting videos', unit='file'):
        input_file = video_file
        relative_path = os.path.relpath(input_file, input_directory)
        output_file = os.path.join(output_directory, relative_path)
        output_file = os.path.splitext(output_file)[0] + '.mp4'
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        convert_to_h264(input_file, output_file)

if __name__ == '__main__':
    input_directory = r'D:\ai-video\太原武宿机场'  # 设置输入目录的路径
    output_directory = r'D:\ai-video\10800'  # 设置输出目录的路径

    convert_videos_in_directory(input_directory, output_directory)
