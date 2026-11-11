import os
import pprint
import requests
import re
from dotenv import load_dotenv

load_dotenv()

def get_video(input_url) :
    regex = r"(?:v=|\/v\/|youtu\.be\/|\/embed\/|\/shorts\/)([a-zA-Z0-9_-]{11})"
    match_video = re.search(regex, input_url)

    if match_video is None :
        return "올바른 주소 아님"

    video_id = match_video.group(1)
    YOUTUBE_API_KEY = os.getenv("KEY")

    url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {
        'part' : 'snippet,statistics',
        'id' : video_id,
        'key' : YOUTUBE_API_KEY
    }
    response = requests.get(url, params = params, timeout = 10).json()

    return response

def get_rest_api_data() :
    url = 'https://rest-api-test-self.vercel.app/api/3'
    response = requests.get(url, timeout = 10).json()

    return response