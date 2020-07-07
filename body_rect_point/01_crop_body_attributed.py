import cv2
import numpy as np

import fnmatch
import os
import shutil
import copy

# """
# 第一步，将质检完标框数据，不可随意更改文件夹目录结构
# 务必按照严格按照示例文件夹名来创建文件夹，在原文件夹名基础之上，创建文件夹名 加 后缀  _drew_rect\01_head
# 202006_01
# 202006_01_drew_rect\01_head

# 待转换数据路径    root = r"C:\Users\wht9787\Desktop\202006_01"
# 合并后数据路径    target = r"C:\Users\wht9787\Desktop\202006_01_drew_rect\01_head"

# """
def is_file_match(filename, patterns):
    """
    判断文件是否符合判定条件 patterns
    :param filename: 目标检测文件名
    :param patterns: 文件对比条件
    :return: 返回判断结果 匹配成功返回True 匹配失败返回False
    """
    for pattern in patterns:
        if fnmatch.fnmatch(filename, pattern):
            return True
    return False


def find_special_files(root, patterns=['*'], exclude_dirs=[], exclude_files=['.DS_Store', 'Thumbs.db']):
    """
    寻找特定文文件夹中各个符合筛选条件文件的路径
    :param root: 文件路径
    :param patterns: 文件类别
    :param exclude_dirs: 排除特定文件夹
    :param exclude_files: 排除特定文件
    :return: 返回文件夹中各个符合筛选条件文件的路径（迭代器）
    """
    for root, dirnames, filenames in os.walk(root):
        for filename in filenames:
            if filename not in exclude_files:
                if is_file_match(filename, patterns):
                    yield os.path.join(root, filename)
        for d in exclude_dirs:
            if d in dirnames:
                dirnames.remove(d)



if __name__ == "__main__":
    root = r"D:\002"
    target = r"D:\555\002"
    
    for item in find_special_files(root, patterns=['*.jpg']):
        print('item', item)
        img_cap=cv2.imdecode(np.fromfile(item,dtype=np.uint8),-1)
        content = []
        print('content_1', content)
        if os.path.exists("{}.txt".format(os.path.splitext(item)[0])):
            
            with open("{}.txt".format(os.path.splitext(item)[0]), 'r', encoding='utf-8') as f:
                
                for line in f.readlines():
                    content.append(eval(line.replace("\n", "")))
            print('content', content)
            try:
                for rect_info in content:
                    img_cap_copy = copy.deepcopy(img_cap)
                    print(rect_info)
                    if 'rect' in rect_info.keys():
                        print( rect_info['rect'])
                        rect = [int(i) for i in rect_info['rect'].split(',')]
                        rect_x_min = rect[0]
                        rect_y_min = rect[1]
                        rect_x_max = rect[2]
                        rect_y_max = rect[3]
                        print('rect',"-- {} {} {} {}".format(rect_x_min, rect_y_min, rect_x_max, rect_y_max))

                        save_path = os.path.join(os.path.dirname(item).replace(root, target), "{}-{}-{}-{}-{}-{}-{}-{}.jpg".format(os.path.basename(item).split('.')[0], rect_info['person_id'], rect_info['type'], rect_info['blur'], rect_x_min, rect_y_min, rect_x_max, rect_y_max))
                        if not os.path.exists(os.path.dirname(save_path)):
                            os.makedirs(os.path.dirname(save_path))
                        print(save_path)
                        if not os.path.exists(save_path):
                            cv2.rectangle(img_cap_copy, (rect_x_min, rect_y_min), (rect_x_max, rect_y_max), (0, 0, 255), 2)
                            cv2.imwrite(save_path, img_cap_copy)
            except Exception as e:
                with open('error.txt', 'a', encoding='utf8') as f:
                    f.write("{}\t{}\n".format(item, e))