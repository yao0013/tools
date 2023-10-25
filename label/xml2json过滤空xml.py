# encoding:utf-8
'''
@author: xxxxx
@project: pythonProject
@file: xml2json过滤空xml.py
@time: 2023/4/24 15:18
@desc:
#注释：
'''
import os
import json
import shutil
import xml.etree.ElementTree as ET
from tqdm import tqdm

def xml_to_coco(input_dir, img_input_dir, output_file, img_output_dir):
    data = {
        "categories": [],
        "images": [],
        "annotations": []
    }

    image_id = 1
    annotation_id = 1
    category_dict = {}
    category_id = 1

    xml_files = [file for file in os.listdir(input_dir) if file.endswith('.xml')]

    for file in tqdm(xml_files, desc="Processing XML files"):
        xml_file = os.path.join(input_dir, file)
        tree = ET.parse(xml_file)
        root = tree.getroot()

        objects = root.findall('object')

        if not objects:
            continue

        img_file_name = root.find('filename').text
        img_file_path = os.path.join(img_input_dir, img_file_name)
        shutil.copy(img_file_path, img_output_dir)

        data["images"].append({
            "id": image_id,
            "file_name": img_file_name
        })

        for obj in objects:
            category_name = obj.find('name').text
            if category_name not in category_dict:
                category_dict[category_name] = category_id
                data["categories"].append({
                    "id": category_id,
                    "name": category_name
                })
                category_id += 1

            bndbox = obj.find('bndbox')
            xmin = int(float(bndbox.find('xmin').text))
            ymin = int(float(bndbox.find('ymin').text))
            xmax = int(float(bndbox.find('xmax').text))
            ymax = int(float(bndbox.find('ymax').text))

            data["annotations"].append({
                "id": annotation_id,
                "image_id": image_id,
                "category_id": category_dict[category_name],
                "bbox": [xmin, ymin, xmax - xmin, ymax - ymin],
                "area": (xmax - xmin) * (ymax - ymin),
                "iscrowd": 0
            })
            annotation_id += 1

        image_id += 1

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

input_dir = r'D:\8\annotations'  # XML文件所在的目录
img_input_dir = r'D:\images'  # 您的图片文件所在的目录。
output_file = r'D:\8\train.json'  # 您希望输出的COCO格式JSON文件的路径。
img_output_dir = r'D:\8\train'  # 您希望将选定的图片文件复制到的新路径。

os.makedirs(img_output_dir, exist_ok=True)

xml_to_coco(input_dir, img_input_dir, output_file, img_output_dir)



