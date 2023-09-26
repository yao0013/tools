import ast
import json, os
from xml.dom.minidom import parse
from tqdm import tqdm
from PIL import Image



def txt2xml(txt_path, xml_path):
    if not os.path.exists(xml_path):
        os.mkdir(xml_path)
    # 建立xml文件框架
    xml_head = '''<annotation>
    	<folder>train</folder>
    	<filename>{}</filename>
    	<source>
    		<database>Unknown</database>
    	</source>
    	<segmented>0</segmented>
        '''
    xml_obj = '''
    <object>
		<name>{}</name>
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<score>{}</score>
		<bndbox>
			<xmin>{}</xmin>
			<ymin>{}</ymin>
			<xmax>{}</xmax>
			<ymax>{}</ymax>
		</bndbox>
	</object>
    '''
    xml_end = '''
    </annotation>
    '''
    cnt = 0

    with open(txt_path, "r", encoding='utf-8') as t:
        bboxs = t.readlines()
        for bbox in bboxs:
            try:
                # if 'face' in bbox:
                #     continue
                # img_info = eval(bbox.split('\t')[-1])  # 图像检测信息
                # print(bbox.split()[-1])
                img_info = ast.literal_eval(bbox.split()[-1]) #eval(bbox.split()[-1])
                # print(img_info)
                img_dir = list(img_info.keys())[0]  # 图像路径 -- 键
                img_name = os.path.split(img_dir)[-1]  # 获取图像文件名
                head = xml_head.format(img_name)

                person_bboxs = img_info[img_dir]
                if not person_bboxs:  #无检测框则过滤
                    continue
                # person_info = img_info[img_dir]
                # person_bboxs = person_info['result']
                obj = ''

                for person_bbox in person_bboxs:
                    label = person_bbox[0]
                    score = person_bbox[-1]  #添加置信度字段
                # print(labels)
                    '''
                    编辑label保留条件
                    '''
                    if score <= 0.4:
                        continue

                    person_point = person_bbox[1:-1]  # 行人框
                    # 计算bbox的左上右下坐标
                    xmin = person_point[0]  # 转为str填入xml_obj
                    ymin = person_point[1]
                    xmax = person_point[2]
                    ymax = person_point[3]


                    obj += xml_obj.format(label, score, xmin, ymin, xmax, ymax)
                    ext = os.path.splitext(img_name)[-1]
                x_p = os.path.join(xml_path, img_name.replace(ext, '.xml'))
                with open(x_p, "w", encoding='utf-8') as xml_f:
                    xml_f.write(head + obj + xml_end)
                cnt += 1
                # print(f"convert success {cnt} xml")

            except Exception as e:
                # print(e)
                continue
        print(f"\n convert success {cnt} xml")



if __name__ == "__main__":
    
    infer_file = r"D:\person.log"    
    xml_path = r"D:\annotations"
    txt2xml(infer_file, xml_path)