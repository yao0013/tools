import os
import base64
import requests
from jinja2 import Template
from PIL import Image
from io import BytesIO

def convert_images_to_base64_and_send(folder_path, server_url):
    global image_base64
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            with open(image_path, "rb") as f:
                image_content = f.read()
            image_base64 = base64.b64encode(image_content).decode("utf-8")
            generate_xml_file(image_path)

def generate_xml_file(image_path):
    # 读取图片文件
    with open(image_path, "rb") as f:
        image_content = f.read()
    image = Image.open(BytesIO(image_content))

    # 发送POST请求
    response = requests.post(server_url, json={
        "image": image_base64
    })
    print(response.json())

    # 解析响应结果
    bbox_values = []
    for bbox in response.json()["box"]:
        bbox_values.append({
            "xmin": bbox["xmin"],
            "ymin": bbox["ymin"],
            "xmax": bbox["xmax"],
            "ymax": bbox["ymax"]
        })
    if bbox_values:
        # 读取XML模板文件
        with open("xml_template.xml", "r") as f:
            xml_template = f.read()

        # 使用Jinja2模板引擎生成XML内容
        template = Template(xml_template)
        xml_content = template.render(bbox_values=bbox_values)

        # 保存生成的XML文件
        xml_filename = os.path.splitext(image_path)[0] + ".xml"
        with open(xml_filename, "w") as f:
            f.write(xml_content)

        print(f"XML文件已生成：{xml_filename}")
    else:
        print("没有提取到数值，不生成XML文件。")

if __name__ == "__main__":
    folder_path = "D:\\test"  # 替换为你的目标文件夹路径
    server_url = "http://192.168.19.220:9090/api/inflet/v1/tasks/e59aae8b-324d-4bee-b69e-7d675fc0fecc/predict"  # 替换为你的服务器URL
    convert_images_to_base64_and_send(folder_path, server_url)