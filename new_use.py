import cv2

# 打开原始视频文件
input_video_path = 'D27_20230623184015.mp4'
cap = cv2.VideoCapture(input_video_path)

# 获取原始视频的基本信息
fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 定义要截取的区域的坐标和尺寸
x, y, width, height = 100, 100, 300, 200

# 创建输出视频编写器
output_video_path = 'output_video.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 从原始帧中截取指定区域
    cropped_frame = frame[y:y + height, x:x + width]

    # 将截取的帧写入输出视频
    out.write(cropped_frame)

    # 显示截取的帧（可选）
    cv2.imshow('Cropped Frame', cropped_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
out.release()
cv2.destroyAllWindows()
