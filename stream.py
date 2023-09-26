import os
import subprocess
import signal
import sys

# 检查输入参数数量
if len(sys.argv) != 3:
    print("请提供输入文件夹路径和推流地址作为参数。")
    print("用法: python stream_script.py <输入文件夹路径> <推流地址>")
    sys.exit(1)

# 设置推流地址
output_url = sys.argv[2]

# 设置输入文件夹路径
input_folder = sys.argv[1]


# 定义终止信号的处理函数
def terminate(signal, frame):
    print("接收到终止信号，停止推流。")
    # 终止ffmpeg进程组
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    sys.exit(0)


# 捕获终止信号并调用处理函数
signal.signal(signal.SIGINT, terminate)
signal.signal(signal.SIGTERM, terminate)

# 遍历输入文件夹
for file in sorted(os.listdir(input_folder)):
    if file.endswith(".mp4"):
        # 提取文件名（不含扩展名）
        filename = os.path.splitext(file)[0]

        # 构造推流命令
        command = [
            "ffmpeg",
            "-re",
            "-i", os.path.join(input_folder, file),
            "-c", "copy",
            "-f", "rtsp",
            "{}".format(output_url)
        ]

        # 执行推流命令
        process = subprocess.Popen(command, preexec_fn=os.setsid)
        process.wait()

# 如果遍历完成，脚本会继续运行到这里
print("全部推流已完成。")
