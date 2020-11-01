"""
This manage_audio.py do the following works:
1. Counting duration of all audio in a directory.
2. Exporting statistics duration of all topic.
"""
import wave
import contextlib
import os
import pandas as pd
import matplotlib.pyplot as plt

def get_all_audio_filenames(dir_name):
    filenames = []
    for r, d, f in os.walk(dir_name):
        for filename in f:
            full_path = os.path.join(r,filename)
            if filename.endswith("wav") or filename.endswith("WAV"):
                filenames.append(full_path)
    return filenames

def get_duration_of_audio_file(file_name):
    duration = 0
    with contextlib.closing(wave.open(file_name,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    duration = duration / 3600
    return duration

def get_duration_of_directory(dir_name):
    audio_filenames = get_all_audio_filenames(dir_name)
    duration = 0
    for audio_filename in audio_filenames:
        duration += get_duration_of_audio_file(audio_filename)
    return duration

'''root_dir/topic_name/audio_folder/audio_file'''
def visualize_topic_duration(root_dir, save_file_name="statistic_topic.csv"):
    data = []
    topic_names = os.listdir(root_dir)
    durations = []
    for topic_name in topic_names:
        duration = get_duration_of_directory(os.path.join(root_dir, topic_name))
        durations.append(duration)
        data.append([topic_name, str(len(os.listdir(os.path.join(root_dir,topic_name)))), str(duration)])
    df = pd.DataFrame(data, columns=["Topic names", "Link saved", "Total durations"])
    df.to_csv(save_file_name, index=False)
    plt.bar(topic_names, durations)
    plt.suptitle('Categorical Plotting')
    plt.xlabel("Topic name")
    plt.ylabel("Hours")
    plt.show()



if __name__ == "__main__":
    print("Start processing")
    visualize_topic_duration("./audio")
    print("Done processing")