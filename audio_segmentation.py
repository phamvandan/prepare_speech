from get_audio_from_url import download_audio_from
from split_audio_base_on_silence import do_splitted, append_zeros_for_index
import os
import pandas as pd
import argparse
import multiprocessing as mp

def main_process(index):
    row = data_url.iloc[index]
    name = str(row["index"])
    if row["download"] == "yes":
        print("Ignore downloaded", row["link"])
        return index, None
    url = row["link"]
    print("Start process", url)

    save_root_path = os.path.join(root, row["type"])
    try:
        if not os.path.exists(save_root_path):
            os.mkdir(save_root_path)
    except:
        a=1
    audio_dir = os.path.join(save_root_path, append_zeros_for_index(int(row["index"])))
    if os.path.exists(audio_dir):
        raise Exception("directory" + audio_dir + " existed")
    try:
        print(name)
        download_audio_from(url, name)
        os.mkdir(audio_dir)
        min_silence_len=150
        silence_thresh=-35
        do_splitted(audio_name=name, save_folder=audio_dir, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    except Exception as e:
        if os.path.exists(audio_dir):
            os.rmdir(audio_dir)
        # if os.path.exists(name):
        #     os.remove(name)
        print("exception occur",e)
        return index, "error"
    # if os.path.exists(name):
    #     os.remove(name)
    print("Done")
    return index, None


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--data_file_name", default="url.csv", help="urls file")
parser.add_argument("-e", "--error_file_name", default="error_url.csv", help="csv file for storing error")
parser.add_argument("-r", "--root", default="./audio", help="folder for save audio")
args = parser.parse_args()
data_file_name = args.data_file_name
error_file_name = args.error_file_name
root = args.root
if not os.path.exists(error_file_name):
    temp = []
    df = pd.DataFrame(temp, columns=["link", "index"])
    df.to_csv(error_file_name, index=False)

if not os.path.exists(data_file_name):
    raise Exception("not exist", data_file_name)

error_url = open(error_file_name, "a")
data_url = pd.read_csv(data_file_name)
length = len(data_url)

if not os.path.exists(root):
    os.mkdir(root)

pool = mp.Pool(mp.cpu_count())
batch_size = 100
i = 0 
while length - i > 0:
    idxs = pool.map(main_process, [index for index in data_url.index.values[i:min(i+batch_size, length)]])

    for idx, error in idxs:
        if error is "error":
            row = data_url.iloc[idx]
            error_url.write(str(row["link"])+","+str(row["index"])+"\n")
            data_url.at[idx, "error"] = "yes"
        data_url.at[idx, "download"] = "yes"

    data_url.to_csv(data_file_name, index=False)
    print("done batch", i)
    i = i + batch_size 

error_url.close()