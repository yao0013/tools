#自动拷贝U盘文件
import os
import shutil
import time

# 指定U盘挂载点
usb_mount_point = f"/media/{os.getlogin()}"

# 指定目标复制目录
destination_directory = "/path/to/destination"

while True:
    # 检测U盘目录下是否存在文件夹
    if any(os.path.isdir(os.path.join(usb_mount_point, item)) for item in os.listdir(usb_mount_point)):
        print("发现U盘目录下存在文件夹，正在复制文件...")

        try:
            # 使用shutil进行文件复制，添加错误处理
            shutil.copytree(usb_mount_point, destination_directory)
            print("复制完成！")
        except Exception as e:
            print(f"复制文件时出现错误: {str(e)}")
            # 可以添加适当的错误处理逻辑，比如记录日志或发送通知

        try:
            # 卸载U盘
            os.system(f"umount {usb_mount_point}")
            print("U盘已卸载。")
        except Exception as e:
            print(f"卸载U盘时出现错误: {str(e)}")
            # 可以添加适当的错误处理逻辑

    else:
        print("等待U盘插入或U盘目录下存在文件夹...")

    # 等待一段时间再检查
    time.sleep(5)
