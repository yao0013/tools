#!/bin/bash

# 检查是否安装了pv工具，如果没有则安装
if ! command -v pv &> /dev/null; then
    echo "pv工具未安装，正在安装..."
    if sudo apt-get install pv -y; then
        echo "pv工具安装成功。"
    else
        echo "无法安装pv工具，请手动安装并重新运行脚本。"
        exit 1
    fi
fi

# 指定目标复制目录
destination_directory="/root/test"

while true; do
    # 指定U盘挂载点
    usb_mount_point="/media/gcloud"

    # 检测U盘目录下是否存在文件夹
    if [ -d "$usb_mount_point"/* ]; then
        echo "发现U盘目录下存在文件夹，正在复制文件..."

        # 使用rsync进行文件复制，添加错误处理
        if rsync -ah --info=progress2 "$usb_mount_point/" "$destination_directory/" | pv -lep -s "$(du -sb "$usb_mount_point" | awk '{print $1}')" > /dev/null; then
            echo "复制完成！"
        else
            echo "复制文件时出现错误。"
            # 可以添加适当的错误处理逻辑，比如记录日志或发送通知
        fi

        # 卸载U盘
        if umount "$usb_mount_point"/*; then
            echo "U盘已卸载。"
        else
            echo "卸载U盘时出现错误。"
            # 可以添加适当的错误处理逻辑
        fi
    else
        echo "等待U盘插入或U盘目录下存在文件夹..."
    fi

    # 等待一段时间再检查
    sleep 5
done

exit 0
