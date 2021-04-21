import pandas as pd
from tqdm import tqdm
import argparse
import os


def hydrate_ids(list_path, save_path='./', split_thres=500000):
    filename = list_path.split('/')[-1][:-4]
    file_idx = filename.split('_')[-1]

    ids_csv = pd.read_csv(list_path, header=None)
    all_ids = list(ids_csv[0])
    ids_count = len(all_ids)
    print('\nTotal tweet ids: {}\n'.format(ids_count))

    ids_txt_dir = os.path.join(save_path, file_idx, 'ids/')
    hydrated_dir = os.path.join(save_path, file_idx, 'hydrated/')

    if not os.path.exists(ids_txt_dir):
        os.makedirs(ids_txt_dir)
    if not os.path.exists(hydrated_dir):
        os.makedirs(hydrated_dir)

    print('Converting to separated list txt files...')
    F = open(ids_txt_dir + filename[:-4] + '-PART-1' + '.txt', 'w')

    with tqdm(total=ids_count) as pbar:
        for i in range(ids_count):
            if i % split_thres == 0 and i > 0:
                F.close()
                F = open(ids_txt_dir + filename[:-4] + '-PART-' + str(int(i / split_thres) + 1) + '.txt', 'w')
            F.write(str(all_ids[i]) + '\n')
            pbar.update(1)
    F.close()

    ids_files = os.listdir(ids_txt_dir)
    for file in ids_files:
        print('Hydrating ' + file + '......')
        os.system('twarc hydrate ' + ids_txt_dir + file + ' > ' + hydrated_dir + file[:-4] + '.jsonl')

    print('All files are hydrated!!!')

    return hydrated_dir

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Define path to ids csv and hydrated file')
    parser.add_argument('--list_path', type=str, help='path to csv file that contains twitter id list')
    parser.add_argument('--save_path', type=str, help='path to save hydrated tweets')
    args = parser.parse_args()

    hydrate_ids(list_path=args.list_path, save_path=args.save_path)
