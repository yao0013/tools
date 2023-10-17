import os
import mysql.connector
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# 连接到数据库
db = mysql.connector.connect(
    host="192.168.19.82",
    user="root",
    password="gcloud123",
    database="hup"
)

# 创建游标对象
cursor = db.cursor()

# 执行SQL查询，检索链接和对应的名称
cursor.execute("SELECT href, text FROM title")

# 获取所有链接和对应的名称
links_and_names = cursor.fetchall()

# 指定要保存视频的目录
download_directory = "/root/test"  # 请替换为实际目录路径

# 创建目录（如果不存在）
if not os.path.exists(download_directory):
    os.makedirs(download_directory)

# 遍历链接和名称，并下载第一个视频
for link, name in links_and_names:
    url = link  # 获取链接的值
    first_video_downloaded = False  # 标志，用于跟踪是否已下载链接的第一个视频

    # 发送HTTP请求获取网页内容
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 使用Beautiful Soup解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找所有带有class="slate-video"的<div>元素
        video_divs = soup.find_all('div', class_='slate-video')

        if video_divs:
            # 仅下载第一个视频
            div = video_divs[0]
            video_url = div.find('video')['src']  # 获取视频的URL

            # 构建本地文件路径使用名称作为文件名
            video_filename = os.path.join(download_directory, f"{name}.mp4")

            # 检查文件是否已存在
            if not os.path.exists(video_filename):
                # 下载视频，并添加进度条
                with requests.get(video_url, stream=True) as video_response:
                    video_response.raise_for_status()
                    total_size = int(video_response.headers.get('content-length', 0))
                    block_size = 1024  # 1KB
                    with open(video_filename, 'wb') as video_file:
                        with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
                            for data in video_response.iter_content(block_size):
                                pbar.update(len(data))
                                video_file.write(data)
                    print(f"Downloaded the first video for {name} to {video_filename}")
                first_video_downloaded = True
            else:
                print(f"First video for {name} already exists: {video_filename}")

    if not first_video_downloaded:
        print(f"No video found for {name}, skipping.")

# 关闭数据库连接
db.close()
