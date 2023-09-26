#统计xml文件的标签
import os
import xml.etree.ElementTree as ET
from collections import defaultdict


def parse_xml(file_path, label_counts):
    tree = ET.parse(file_path)
    root = tree.getroot()

    for label_element in root.findall(".//name"):
        label_value = label_element.text
        if label_value:
            label_counts[label_value] += 1


def count_labels_in_directory(directory_path):
    label_counts = defaultdict(int)

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".xml"):
                file_path = os.path.join(root, file)
                parse_xml(file_path, label_counts)

    return label_counts


if __name__ == "__main__":
    directory_path = "D:\\ai-video\\0922\\"
    label_counts = count_labels_in_directory(directory_path)

    for name, count in label_counts.items():
        print(f"Label: {name}, Count: {count}")
