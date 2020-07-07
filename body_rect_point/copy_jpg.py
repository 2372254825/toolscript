import fnmatch
import os
import shutil


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
    # 将原始图拷贝到人员质检目录下
    root = r"\\dtc-fs\SmartCar\DMS_Train\Rear_Seat_Body_Detection_Taxi\2_tobemarked\202004_02_01_drew_rect_result"
    target = r"\\dtc-fs\SmartCar\DMS_Train\Rear_Seat_Body_Detection_Taxi\2_tobemarked\202004_02_01_rect_back_result_split_id"
    jpg_list = [item for item in find_special_files(root, patterns=['*.jpg'], exclude_dirs=[], exclude_files=['.DS_Store', 'Thumbs.db'])]
    for txt in find_special_files(target, patterns=['*.txt'], exclude_dirs=[], exclude_files=['.DS_Store', 'Thumbs.db']):
        target_path = os.path.splitext(txt)[0] + ".jpg"
        target_basename = os.path.splitext(os.path.basename(txt))[0]
        for jpg_path in jpg_list:
            if target_basename in jpg_path:
                shutil.copy(jpg_path, target_path)
                print("{}  {}".format(jpg_path, target_path))
        
