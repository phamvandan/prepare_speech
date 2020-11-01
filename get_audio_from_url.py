from __future__ import unicode_literals
import youtube_dl, pafy, os
from urllib.parse import urlparse, parse_qs

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

def download_audio_from(url, name="temp"):
    url = get_yt_video_id(url)
    ydl_opts = {
        'format': 'bestaudio/best',
        'prefer_ffmpeg': True,
        'keepvideo': False
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    filenames = os.listdir("./")
    for filename in filenames:
        if url in filename: 
            print(filename, name)
            os.rename(filename, name)
            break
        
# import pafy,os

# def download_audio_from(url,name="temp"):
#     video = pafy.new(url) 
#     streams = video.audiostreams
#     print(streams)
#     best = video.getbestaudio() 
#     # Download the video 
#     best.download(filepath=name)

if __name__ == "__main__":
    download_audio_from("https://www.youtube.com/watch?v=e5CKAq1QMLw&list=PL6MWgaszXrMuWZV48Bwo6QH_zaaVuFlJ2&index=24")
    # os.rename("✅ [Phần 3] Dạy Con Trưởng Thành - Bố Mẹ Thường Dạy Con Kiểu Gì  _ Trần Việt Quân-KsgAZz-xfXQ.webm", "temp")
