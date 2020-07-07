import fnmatch
import os
import shutil

"""
第二步，标注关键点完成以后使用此脚本，不可随意更改文件夹目录结构
务必按照严格按照示例文件夹名来创建文件夹，在 _drew_rect 文件夹名基础之上，创建文件夹名 加 后缀  _result
202006_01_02_drew_rect
202006_01_02_drew_rect_result

待转换数据路径    root = r"\\dtc-fs\SmartCar\DMS_Train\Rear_Seat_Body_Detection_Taxi\2_tobemarked\202006_01_02_drew_rect"
合并后数据路径    target = r"\\dtc-fs\SmartCar\DMS_Train\Rear_Seat_Body_Detection_Taxi\2_tobemarked\202006_01_02_drew_rect_result"

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

class_names = {"_ls":"left_shoulder", "_rs":"right_shoulder", "_lc":"left_crotch", "_rc":"right_crotch", "_head":"head", "_neck":"neck"}
class_dirnames = ["01_head", "02_neck", "03_ls", "04_rs", "05_lc", "06_rc"]



if __name__ == "__main__":
    root = r"\\dtc-fs\SmartCar\DMS_Train\Rear_Seat_Body_Detection_Taxi\2_tobemarked\202006_01_02_drew_rect"
    target = r"\\dtc-fs\SmartCar\DMS_Train\Rear_Seat_Body_Detection_Taxi\2_tobemarked\202006_01_02_drew_rect_result"
    img_marked_list = {}
    for item in find_special_files(root, patterns=["*.txt"], exclude_dirs=[], exclude_files=['.DS_Store', 'Thumbs.db']):
        #print(item)
        persion_id = os.path.basename(item).split("-")[1]
        #print(persion_id)
        # """C:\Users\wht9787\Desktop\202004_02_01_drew_rect_small\01_head\20200409\adult\vdo_0000000025_0000000001_00000-01-adult-not_blur-181-192-866-1078"""
        body_part_dir = item.replace(root, "").split("\\")[1]
        #print(body_part_dir)
        
        class_img_name = os.path.join(os.path.dirname(item).replace(root, target), os.path.basename(item).split("-")[0] + ".jpg")
        img_name = class_img_name.replace("\\" + body_part_dir, "")
        #print(img_name)

        if img_name not in img_marked_list.keys():
            img_marked_list[img_name] = []
        print(img_name)
        rect_position = "{},{},{},{}".format(os.path.basename(item).split("-")[-4],os.path.basename(item).split("-")[-3],os.path.basename(item).split("-")[-2],os.path.basename(os.path.splitext(item)[0]).split("-")[-1])
        rect_content = {"person_id":persion_id,"type":os.path.basename(item).split("-")[2],"blur":os.path.basename(item).split("-")[3],"body_part":"none","point_visible":"none","rect":rect_position,"shape_type":"rect",}
        if rect_content not in img_marked_list[img_name]:
            img_marked_list[img_name].append(rect_content)
        for part_name in class_names.keys():
            if part_name in body_part_dir:
                print(class_names[part_name])
                print(item)
                with open(item, "r", encoding="utf-8") as f:
                    item_content = eval(f.read().split("\n")[0])
                    """{"body_part":"left_shoulder","shape_type":"point","points":"1","point0":"1584,1117"}

                    {"point_visible":"visible","shape_type":"point","points":"1","point0":"291,260"}
                    
                    {"person_id":"02","type":"child","blur":"blur","body_part":"none","point_visible":"none","rect":"1557,685,1920,1080","shape_type":"rect",}
                    {"person_id":"01","type":"none","blur":"none","body_part":"head","point_visible":"visible","shape_type":"point","points":"1","point0":"401,506"}
                    need person_id 
                        point_visible
                        body_part
                        type
                        blur
                    """
                item_content["person_id"] = persion_id
                item_content["body_part"] = class_names[part_name]
                print(item_content)
                
                if item_content["shape_type"] == "point":
                    item_content["blur"] = "none"
                    item_content["type"] = "none"
                elif item_content["shape_type"] == "rect":
                    item_content["body_part"] = "none"
                    item_content["point_visible"] = "none"
                img_marked_list[img_name].append(item_content)

    # print(img_marked_list)

    for img in img_marked_list.keys():
        save_path = os.path.splitext(img)[0] + ".txt"
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))
        with open(save_path, 'w', encoding='utf-8') as f:
            for line in img_marked_list[img]:
                f.write('{}\n'.format(str(line).replace("'", '"')))    

        





