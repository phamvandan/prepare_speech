from urllib.parse import urlparse, parse_qs
import json
from urllib.request import urlopen
import googleapiclient.discovery
import pafy
import pandas as pd
import urllib

def get_urls_by_playist(url):
    playlist = pafy.get_playlist(url) 
  
    # getting playlist items 
    items = playlist["items"] 
    urls = []
    # selecting single item 
    for item in items:
        # getting pafy object 
        i_pafy = item['pafy'] 
            
        # getting watch url 
        y_url = i_pafy.watchv_url 
        
        urls.append(y_url)
    return urls 

def get_yt_video_id(url):
    """Returns Video_ID extracting from the given url of Youtube
    
    Examples of URLs:
      Valid:
        'http://youtu.be/_lOT2p_FCvA',
        'www.youtube.com/watch?v=_lOT2p_FCvA&feature=feedu',
        'http://www.youtube.com/embed/_lOT2p_FCvA',
        'http://www.youtube.com/v/_lOT2p_FCvA?version=3&amp;hl=en_US',
        'https://www.youtube.com/watch?v=rTHlyTphWP0&index=6&list=PLjeDyYvG6-40qawYNR4juzvSOg-ezZ2a6',
        'youtube.com/watch?v=_lOT2p_FCvA',
      
      Invalid:
        'youtu.be/watch?v=_lOT2p_FCvA',
    """
    if url.startswith(('youtu', 'www')):
        url = 'http://' + url
        
    query = urlparse(url)
    
    if 'youtube' in query.hostname:
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        elif query.path.startswith(('/embed/', '/v/')):
            return query.path.split('/')[2]
    elif 'youtu.be' in query.hostname:
        return query.path[1:]
    else:
        raise ValueError

def get_duration(video_id, api_key):
    searchUrl="https://www.googleapis.com/youtube/v3/videos?id="+video_id+"&key="+api_key+"&part=contentDetails"
    response = urlopen(searchUrl).read()
    data = json.loads(response)
    all_data=data['items']
    contentDetails=all_data[0]['contentDetails']
    duration=contentDetails['duration']
    duration = duration_converter_to_minute(duration)
    return duration

def duration_converter_to_minute(old_dur):
    temp = old_dur[2:]
    hour=0
    minute=0
    if "H" in temp:
        hour = int(temp.split("H")[0])
        temp = temp.split("H")[1]
    if "M" in temp:
        minute = int(temp.split("M")[0])
        temp = temp.split("M")[1]
        
    return hour*60 + minute


def data_extract_from_playist_url(url):
    video_id = get_yt_video_id(url)
    api_key = "AIzaSyCxv27mYNR7wN5oPNlElVBcib5AIGFXV0E"
    duration = get_duration(video_id, api_key)
    return [url, duration]

import datetime, os

def name_random(name="data"):
    if not os.path.exists("./" + name):
        os.mkdir("./"+name)
    i = datetime.datetime.now()
    return name + "/" + "{}{}{}".format(i.minute, i.second, i.microsecond)+".csv"

import multiprocessing as mp
import sys
import re


def get_urls_from_search(textToSearch):
    query = urllib.parse.quote(textToSearch)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    video_ids = re.findall(r"watch\?v=(\S{11})", response.read().decode())
    for i in range(len(video_ids)):
        video_ids[i] = "https://www.youtube.com/watch?v=" + video_ids[i]
    urls = video_ids
    return urls

def result_from_playist():
    playist_url = sys.argv[1]
    ## playist url
    urls = get_urls_by_playist(playist_url)
    # urls = urls[151:]
    pool = mp.Pool(mp.cpu_count())
    print("starting")
    data = pool.map(data_extract_from_playist_url, [url for url in urls])
    print("total", len(data))
    dataframe = pd.DataFrame(data, columns=['link', 'duration'])
    # dataframe.to_csv(name_random())
    dataframe.to_csv("result.csv")
    print("done")

def result_from_search(textToSearch):
    ## playist url
    urls = get_urls_from_search(textToSearch)
    urls = urls[:5]
    pool = mp.Pool(mp.cpu_count())
    print("starting")
    data = pool.map(data_extract_from_playist_url, [url for url in urls])
    print("total", len(data))
    dataframe = pd.DataFrame(data, columns=['link', 'duration'])
    # dataframe.to_csv(name_random())
    dataframe.to_csv("result.csv")
    print("done")


if __name__ == "__main__":
    f = open("search_query.txt", "r+")
    query_string = f.readlines()[0]
    if query_string.strip()=="":
        raise  EnvironmentError("Please insert the query string in search_query.txt")
    print("query_string=", query_string)
    result_from_search(query_string)