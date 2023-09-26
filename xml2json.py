import json, os
from PIL import Image
from xml.dom.minidom import parse
from tqdm import tqdm
def xml2json(xml_path, jsonfile,img_path):
    
    cat2id, img2id = {}, {}
    categories = []
    images = []
    annotations = []
    cat_count, img_count, ann_count = 0, 0, 0

    xmls = os.listdir(xml_path)
    for xml in tqdm(xmls):
        # print(xml)
        root = parse(os.path.join(xml_path, xml))
        filename = root.getElementsByTagName('filename')[0].firstChild.data #获取xml中的文件名

        # 为防止原xml中的filename有改动，改成与xml对应的图片文件名
        name, ext = os.path.splitext(filename)
        # print(name, ext)
        filename = xml.replace('.xml', ext)

        '''
        编辑图片
        '''
        if img_path is not None:
            f_p = os.path.join(img_path, filename)
            img = Image.open(f_p)
            W, H = img.size

        if filename not in img2id:
            img2id[filename] = img_count
            # size = root.getElementsByTagName('size')[0]
            # width = float(size.getElementsByTagName('width')[0].firstChild.data)
            # height = float(size.getElementsByTagName('height')[0].firstChild.data)
            images.append(dict(file_name=filename, id=img2id[filename]))
            img_count += 1  #迭代img_id

        objects = root.getElementsByTagName('object')  #检测框信息

        for obj in objects:  #一张图有多个object（检测框）

            try:
                cat = obj.getElementsByTagName('name')[0].firstChild.data
                # label = ['phone']
                # # if len(cat)==0:
                # #     continue
                # if cat not in label:
                #     continue

                '''
                此处可对类别进行预处理
                '''

            # bbox = obj.getElementsByTagName('bndbox')[0]
                xmin = int(float(obj.getElementsByTagName('xmin')[0].firstChild.data))
                ymin = int(float(obj.getElementsByTagName('ymin')[0].firstChild.data))
                xmax = int(float(obj.getElementsByTagName('xmax')[0].firstChild.data))
                ymax = int(float(obj.getElementsByTagName('ymax')[0].firstChild.data))
                '''
                此处可对框标注信息进行处理
                '''
                # w, h = xmax-xmin, ymax-ymin
                # area=w*h
                # if area / (W*H) < 0.00028:
                #     continue
            except Exception as e:
                continue


            if cat not in cat2id: # category_id
                cat2id[cat] = cat_count
                categories.append(dict(id=cat_count, name=cat))
                cat_count += 1
            ann = dict(id=ann_count, image_id=img2id[filename], category_id=cat2id[cat],
                     bbox=[xmin, ymin, xmax-xmin, ymax-ymin],
                    area=(xmax - xmin) * (ymax - ymin))
                    #  bbox=[xmin, ymin, xmax, ymax],
                    # area=xmax * ymax)
            annotations.append(ann)
            ann_count += 1

    with open(jsonfile, 'w', encoding='utf-8') as f:
        json_infos = dict(categories=categories, images=images, annotations=annotations)
        json.dump(json_infos, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # 路径
    img_path= r"D:\8\images"   # 原始图片的路径
    xml_path = r"D:\8\annotations"
    jsonfile = r"D:\train.json"
    xml2json(xml_path, jsonfile, img_path)
#keyint