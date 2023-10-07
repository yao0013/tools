import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import logging
import os
import shutil
import zipfile

# 设置日志记录
logging.basicConfig(filename='download_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 设置文件夹路径
output_folder = 'output'  # 输出文件夹的路径
os.makedirs(output_folder, exist_ok=True)  # 如果文件夹不存在则创建

# 读取Excel文件
excel_file = '10.xlsx'  # 替换成你的Excel文件路径
df = pd.read_excel(excel_file)
download_count = 0

# 存储所有下载的文件的文件名
downloaded_files = []

# 遍历Excel的第一列（URL列）和第二列（命名列）
for index, row in df.iterrows():
    url = row[0]  # 第一列的URL
    name_col2 = row[1]  # 第二列的字符
    name_col4 = row[3]  # 第四列的字符

    # 发送HTTP请求下载图片
    response = requests.get(url)

    # 检查响应状态码
    if response.status_code == 200:
        # 读取图片内容
        image_data = BytesIO(response.content)

        # 构造文件名，以第二列字符加下划线加第四列字符作为文件名
        file_name = f'{name_col2}_{name_col4}.jpg'
        file_path = os.path.join(output_folder, file_name)

        # 打开图片并保存
        with Image.open(image_data) as img:
            img.save(file_path)
            logging.info(f'Saved {file_name}')
            download_count += 1
            print(f'Saved {file_name}')
            downloaded_files.append(file_path)

    else:
        logging.error(f'Failed to download image from {url}')
        print(f'Failed to download image from {url} for {name_col2}')

logging.info(f'Downloaded {download_count} images')
print(f'Downloaded {download_count} images')

# 创建压缩文件
zip_file_name = 'downloaded_images.zip'
with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file in downloaded_files:
        zipf.write(file, os.path.basename(file))

# 移动压缩文件到指定路径
zip_file_path = os.path.join(output_folder, zip_file_name)
shutil.move(zip_file_name, zip_file_path)


logging.info(f'Created {zip_file_name}')
logging.info('Done')
print('Done')