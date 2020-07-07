import fnmatch
import os
import shutil

"""
第三步，标注关键点完成以后使用此脚本，不可随意更改文件夹目录结构
务必按照严格按照示例文件夹名来创建文件夹，在 _drew_rect 文件夹名基础之上，创建文件夹名 加 后缀  _split_id
202006_01_02_drew_rect
202006_01_02_drew_rect_split_id

img_root = r"\\dtc-fs\SmartCar\DMS_Train\Rear_Seat_Body_Detection_Taxi\2_tobemarked\202006_01_02"
root = r"\\dtc-fs\SmartCar\DMS_Train\Rear_Seat_Body_Detection_Taxi\2_tobemarked\202006_01_02_drew_rect_result"
target = r"\\dtc-fs\SmartCar\DMS_Train\Rear_Seat_Body_Detection_Taxi\2_tobemarked\202006_01_02_drew_rect_split_id"

原图片路径      img_root = r"\\dtc-fs\SmartCar\DMS_Train\Rear_Seat_Body_Detection_Taxi\2_tobemarked\202006_01_02"
待转换数据路径    root = r"\\dtc-fs\SmartCar\DMS_Train\Rear_Seat_Body_Detection_Taxi\2_tobemarked\202006_01_02_drew_rect"
合并后数据路径    target = r"\\dtc-fs\SmartCar\DMS_Train\Rear_Seat_Body_Detection_Taxi\2_tobemarked\202006_01_02_drew_rect_split_id"

"""

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
    img_root = r"\\dtc-fs\SmartCar\DMS_Train\Rear_Seat_Body_Detection_Taxi\2_tobemarked\202006_01_02"
    root = r"\\dtc-fs\SmartCar\DMS_Train\Rear_Seat_Body_Detection_Taxi\2_tobemarked\202006_01_02_drew_rect_result"
    target = r"\\dtc-fs\SmartCar\DMS_Train\Rear_Seat_Body_Detection_Taxi\2_tobemarked\202006_01_02_drew_rect_split_id"
    img_list_person = {}
    for txt_item in find_special_files(root, patterns=['*.txt'], exclude_dirs=['原始'], exclude_files=['.DS_Store', 'Thumbs.db']):
        person_id = {"01":[], "02":[], "03":[], "04":[], "05":[], "06":[],}
        with open(txt_item, "r", encoding="utf-8") as f:
            for line in f.readlines():
                line_dict = eval(line.replace("\n", ""))
                if line_dict["person_id"] == "01":
                    person_id["01"].append(line_dict)
                elif line_dict["person_id"] == "02":
                    person_id["02"].append(line_dict)
                elif line_dict["person_id"] == "03":
                    person_id["03"].append(line_dict)
                elif line_dict["person_id"] == "04":
                    person_id["04"].append(line_dict)
                elif line_dict["person_id"] == "05":
                    person_id["05"].append(line_dict)
                elif line_dict["person_id"] == "06":
                    person_id["06"].append(line_dict)
        img_list_person[txt_item] = person_id
    # print(img_list_person)

    # 测试人员点和框的完整性
    # count = 0
    # with open("img_review_list.txt", "w", encoding="utf8") as f:
    #     for img in img_list_person.keys():
    #         for id in img_list_person[img].keys():
    #             if len(img_list_person[img][id]) != 7 and len(img_list_person[img][id]) != 0:
    #                 count += 1
    #                 f.write("{}\n".format(img))
    #                 print("{} {} {}".format(count, img,  img_list_person[img][id]))

    # 按照人员ID的质检

    

    img_list=[img for img in find_special_files(img_root, patterns=['*.jpg'], exclude_dirs=[], exclude_files=['.DS_Store', 'Thumbs.db'])]

    for item in img_list_person.keys():
        print(item)
        for id in img_list_person[item].keys():
            if img_list_person[item][id] !=[]:
                if not os.path.exists(os.path.dirname(os.path.join(os.path.dirname(item).replace(root, target), os.path.splitext(os.path.basename(item))[0], id, os.path.basename(item)))):
                    os.makedirs(os.path.dirname(os.path.join(os.path.dirname(item).replace(root, target), os.path.splitext(os.path.basename(item))[0], id, os.path.basename(item))))
                txt_path = os.path.join(os.path.dirname(item).replace(root, target), os.path.splitext(os.path.basename(item))[0], id, os.path.basename(item))
                with open(txt_path, "w", encoding="utf8") as f: 
                    for line in img_list_person[item][id]:
                        f.write(str(line).replace("'", '"'))
                        f.write("\n")
                raw_img_path = os.path.splitext(os.path.dirname(os.path.dirname(txt_path.replace(target, img_root))))[0] + ".jpg"
                print("raw img path == {}".format(raw_img_path))
                shutil.copy(raw_img_path, os.path.splitext(txt_path)[0] + ".jpg")

        

        
            
        
