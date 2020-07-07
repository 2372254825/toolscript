import fnmatch
import os
import shutil

"""
最后步骤，将质检完splitID的数据合并起来，合并为递交状态。
务必按照严格按照示例文件夹名来创建文件夹，在split_id 文件夹名基础之上，创建文件夹名 加 后缀  _meraged
202006_01_02_drew_rect_split_id
202006_01_02_drew_rect_split_id_meraged

待转换数据路径    root = r"\\dtc-fs\SmartCar\DMS_Train\Rear_Seat_Body_Detection_Taxi\2_tobemarked\202006_01_02_drew_rect_split_id"
合并后数据路径    target = r"\\dtc-fs\SmartCar\DMS_Train\Rear_Seat_Body_Detection_Taxi\2_tobemarked\202006_01_02_drew_rect_split_id_meraged"

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

# gunicorn toolkit.wsgi:application -w 4 -k gthread -b 127.0.0.1:19550 --max-requests=10000


if __name__ == "__main__":
    # 最后步骤，将质检完splitID的数据合并起来，合并为递交状态。

    root = r"\\dtc-fs\SmartCar\DMS_Train\Rear_Seat_Body_Detection_Taxi\2_tobemarked\202006_01_02_drew_rect_split_id"
    target = r"\\dtc-fs\SmartCar\DMS_Train\Rear_Seat_Body_Detection_Taxi\2_tobemarked\202006_01_02_drew_rect_split_id_meraged"

    img_dict = {}
    for txt_item in find_special_files(root, patterns=['*.txt'], exclude_dirs=[], exclude_files=['.DS_Store', 'Thumbs.db']):
        if os.path.dirname(os.path.dirname(txt_item)).replace(root, target) not in img_dict.keys():
            img_dict[os.path.dirname(os.path.dirname(txt_item)).replace(root, target)] = []
        img_dict[os.path.dirname(os.path.dirname(txt_item)).replace(root, target)].append(txt_item)
    # print(img_dict)

    for item in img_dict.keys():
        txt_content = []
        for txt in img_dict[item]:
            with open(txt, 'r', encoding='utf8') as f:
                for line in f.readlines():
                    txt_content.append(line)
        print(item)
        if not os.path.exists(os.path.dirname(item)):
            os.makedirs(os.path.dirname(item))
        # print(item)
        with open(item + ".txt", 'w', encoding='utf8') as f:
            for line in txt_content:
                f.write(line.replace("'", '"'))
        