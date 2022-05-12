import os
from os import path


# md文件扫描
def __scaner_files(results, file_path, exclude_folders=[]):
    file = os.listdir(file_path)
    for f in file:
        real_path = path.join(file_path, f)
        if path.isfile(real_path):
            if path.basename(real_path).endswith('.md'):
                results.append(path.abspath(real_path))
            # 如果是文件，则保存绝对路径
        elif path.isdir(real_path):
            # 如果是目录，则是递归
            if path.basename(real_path) in exclude_folders:
                continue
            else:
                __scaner_files(results, real_path, exclude_folders)
        else:
            print("error")


def scan_files(file_path, exclude_folders):
    results = []
    __scaner_files(results, file_path, exclude_folders)
    return results
