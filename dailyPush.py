import requests
import json
import os
import time

# BARK_API = os.environ.get("BARK_API")
# PODCAST_HOT_EPISODES_API = os.environ.get("PODCAST_HOT_EPISODES")

BARK_API = "https://api.day.app/hoT3H6LmihHPftm4MFGqFX"
PODCAST_HOT_EPISODES_API = "https://xyzrank.com/assets/hot-episodes.24ef12b57741554e245e301ea9240f8f.json"

def get_podcast_info(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"request error: {e}")
    except ValueError:
        print("cannot parse json data!")

data = get_podcast_info(PODCAST_HOT_EPISODES_API)


top_10_episodes = data["data"]["episodes"][:6]


def push_ios_notification(url, data):
    try:
        json_data = json.dumps(data)
        headers = {
            "Content-Type": "application/json; charset=utf-8"
        }
        response = requests.post(url, data=json_data, headers=headers)
        
        if response.status_code == 200:
            print("post done!")
        else:
            print(f"post failed, code: {response.status_code}")
            print("resp: ", response.text)
    
    except requests.RequestException as e:
        print(f"err: {e}")
    except ValueError:
        print("cannot parse json data!")


for episode in top_10_episodes:
    data = {
        "body": episode["title"],
        "title": episode["podcastName"],
        "category": "myNotificationCategory",
        "icon": episode["logoURL"],
        "group": "podcast",
        "url": "https://xyzrank.com/#/"
    }
    push_ios_notification(BARK_API, data)
    time.sleep(0.2)
