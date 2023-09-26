import os
from tqdm import tqdm
from PIL import Image

def get_crop_img(infer_txt, img_path, new_dir, add=2):
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    txts = open(infer_txt, "r", encoding='utf-8').readlines()
    img_names = []
    points = []
    for txt in tqdm(txts):
        try:
            img_info = eval(txt.split()[-1])
            img_dir = list(img_info.keys())[0] 
            img_name = os.path.split(img_dir)[-1]  

            one_bboxs = img_info[img_dir]  
            if not one_bboxs:  
                continue
            thresh = 0
            for k, one_bbox in enumerate(one_bboxs):
                if one_bbox[-1]<0.8:
                    continue

                person_point = one_bbox[1:-1]  
                xmin = person_point[0]
                ymin = person_point[1]
                xmax = person_point[2]
                ymax = person_point[3]
               
                x, y = xmin, ymin
                img = Image.open(os.path.join(img_path, img_name))
                width, height = img.size
                W, H = xmax-xmin, ymax-ymin
                w, h = W, H
                
                n = add - 1
                xmin -= n*W//2
                ymin -= n*H//2
                xmax += n*W//2
                ymax += n*H//2

                if xmin < 0:
                    xmin = 0
                   
                if ymin < 0:
                    ymin = 0
                    

                if xmax > width:
                    xmax = width
                   
                if ymax > height:
                    ymax = height

                new_person_point = [xmin, ymin, xmax, ymax]              
                new_img = img.crop(tuple(new_person_point))
                name, ext = os.path.splitext(img_name)
                Img_name = name + f'-x{x}-y{y}-w{w}-h{h}' + '.jpg'
                new_name = os.path.join(new_dir, Img_name)
                new_img.save(new_name,quality=95)


        except Exception as e:
            print(e)
            continue

if __name__ == "__main__":
    infer_txt = r"D:\视频素材\0816\head.log"
    img_path = r"D:\视频素材\0816"
    new_dir = r"D:\视频素材\0816\new"
    get_crop_img(infer_txt, img_path, new_dir,add=1.5)