import os
import time

def find_new_list(id_list_path,readed_files):
    if not os.path.exists(readed_files):
        readed_list = []
    else:
        readed_list = []
        with open(readed_files,'r') as f:
            for line in f.readlines():
                readed_list.append(line.strip('\n'))

    all_file_ = get_by_time(id_list_path)
    all_file = [os.path.basename(path) for path in all_file_]
    readed_set = set(readed_list)
    all_file_ = set(all_file)

    if all_file_ != readed_set:
        diff = all_file_ - readed_set
        for file_ in diff:
            with open(readed_files, "a") as f:
                f.write(str(file_) + "\n")
            f.close()
        return [os.path.join(id_list_path,file_path) for file_path in diff]
    
    else:
        return False

def get_by_time(dir_path, reverse=True):
    file_paths = os.listdir(dir_path)
    if len(file_paths) <= 0:
        return []
    else:
        sorted_file_list = sorted(file_paths, key=lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(os.path.join(dir_path,x)))), reverse=reverse)
        sorted_file_list_filtered = []
        for i in range(len(sorted_file_list)):
            file = sorted_file_list[i]
            if file[0:4] == 'coro':
                sorted_file_list_filtered.append(file)
        return sorted_file_list_filtered[0:]
