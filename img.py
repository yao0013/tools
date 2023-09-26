import os
import base64
import requests
import json
from jinja2 import Template


def image_to_base64(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def convert_images_to_base64_and_send(folder_path, server_url):
    image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
    global base64_data
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith(tuple(image_extensions)):
                base64_data = image_to_base64(file_path)
                print(f"File: {file_path}")
                #print(f"Base64 Data: {base64_data}\n")
                #发送Base64数据到服务器
                send_to_server(base64_data, server_url)


def send_to_server(base64_data, server_url):
    headers = {"Content-Type": "application/json"}
    data = "{\"image\": \"data:image/jpeg;base64,"+base64_data+"\"}"
    #print(data)

    try:
        response = requests.put(server_url, data=data, headers=headers)
        if response.status_code == 200:
            print("Base64 data sent successfully to the server.")
            print(response.text)

        else:
            print("Failed to send Base64 data to the server. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error sending request to the server:", str(e))
    return response.text

#提取数值函数

def get_point():
    data_dict = send_to_server(base64_data, server_url)
    # 将字符串转换为字典
    data_dict = json.loads(data_dict)
    # 提取多个bbox节点
    bbox_nodes = data_dict["data"]["targets"]

    # 存储提取的数值
    bbox_values = []

    # 遍历每个bbox节点，并提取数值
    for bbox_node in bbox_nodes:
        left_top_x = int(bbox_node["bbox"]["box"]["left_top_x"])
        left_top_y = int(bbox_node["bbox"]["box"]["left_top_y"])
        right_bottom_x = int(bbox_node["bbox"]["box"]["right_bottom_x"])
        right_bottom_y = int(bbox_node["bbox"]["box"]["right_bottom_y"])

        # 将数值存储到bbox_values字典中
        bbox_values.append({
            "left_top_x": left_top_x,
            "left_top_y": left_top_y,
            "right_bottom_x": right_bottom_x,
            "right_bottom_y": right_bottom_y
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

            print("XML文件已生成：generated_xml_file.xml")
        else:
            print("没有提取到数值，不生成XML文件。")

if __name__ == "__main__":
    folder_path = "D:\\test"  # 替换为你的目标文件夹路径
    server_url = "http://192.168.19.220:9090/api/inflet/v1/tasks/e59aae8b-324d-4bee-b69e-7d675fc0fecc/predict"  # 替换为你的服务器URL
    convert_images_to_base64_and_send(folder_path, server_url)
    get_point()
