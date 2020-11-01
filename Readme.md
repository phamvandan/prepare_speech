## Preparing the audio links from YOUTUBE.
# Installation
* Create python3 virtual environment for this project.
``` 
    sudo apt-get install python3-venv 
    sudo python3 -m venv prepare_speech_venv
```
* Installing requirements.
```
    source prepare_speech_venv/bin/activate
    pip install -r requirements.txt
```
# How to run
* Activate the environment.
```
    source prepare_speech_venv/bin/activate
```
* **Get all links from a youtube playlist url**.
```
    python get_link_and_duration_from_playist.py + playlist url
    Example:
    python get_link_and_duration_from_playist.py https://www.youtube.com/playlist\?list\=PL4l9KtZCNZkvkRCkANNnhp_EGhfRia-Fv
```
Results are stored in a file named **result.csv**.
* **Get all links from a search query**.  
Step 1: Insert a query in the *search_query*.txt.  
Step 2: Run this command.
```
    python get_link_and_duration_from_search.py
```
Results are stored in a file named **result.csv**.
