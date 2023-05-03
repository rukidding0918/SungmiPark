import os



def get_dir_list(path):
    dirs = []
    for dir in os.listdir(path):
        if os.path.isdir(os.path.join(path, dir)):
            dirs.append(dir)
    return dirs


def get_file_list(path):
    files = []
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            files.append(file)
    return files