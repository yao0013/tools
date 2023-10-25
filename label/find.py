#找到指定标签的XML文件
import os
import xml.etree.ElementTree as ET


def find_xml_files_with_name(folder_path, target_name):
    found_files = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            xml_path = os.path.join(folder_path, filename)
            tree = ET.parse(xml_path)
            root = tree.getroot()

            for element in root.iter():
                if element.tag == "name" and element.text == target_name:
                    found_files.append(filename)
                    break  # No need to continue searching in this file

    return found_files


if __name__ == "__main__":
    folder_path = "D:\\视频素材\\0811\\"
    target_name = "no_helmet"

    found_files = find_xml_files_with_name(folder_path, target_name)

    if found_files:
        print("找到以下文件：")
        for filename in found_files:
            print(filename)
    else:
        print("未找到匹配的文件。")
