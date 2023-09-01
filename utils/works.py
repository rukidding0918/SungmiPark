import os



def get_dir_list(path):
    years = []
    others = []
    for dir in os.listdir(path):
        if os.path.isdir(os.path.join(path, dir)):
            if dir.isnumeric():
                years.append(dir)
            else:
                others.append(dir)
    years.sort(reverse=True)
    others.sort()
    return years + others


def get_file_list(path):
    files = []
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            files.append(file)
    files.sort()
    return files