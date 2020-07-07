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
    print("此脚本功能是批量移动文件夹下面的Thumbs.db文件")
    input_path_1 = input("输入待处理路径：  ")
    dir_path = r"{}".format(input_path_1)
    input_path_2 = input("输入目标路径：  ")
    target_path = r"{}".format(input_path_2)

    count = 0
    for db_file in find_special_files(dir_path, patterns=['Thumbs.db'], exclude_dirs=[], exclude_files=[]):
        count += 1
        target_file_path = db_file.replace(dir_path, target_path)
        if not os.path.exists(os.path.dirname(target_file_path)):
            os.makedirs(os.path.dirname(target_file_path))
        shutil.move(db_file, target_file_path)
        print("{} --> {} ".format(count, target_file_path.replace(target_path, "")))
    
    input("移动完毕，按任意键结束程序")