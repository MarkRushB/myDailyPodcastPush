import requests
import json
import os

BARK_API = os.environ.get("BARK_API")
PODCAST_HOT_EPISODES_API = os.environ.get("PODCAST_HOT_EPISODES")

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

print(data["data"]["episodes"][0])


def push_ios_notification(url, data):
    try:
        json_data = json.dumps(data)
        headers = {
            "Content-Type": "application/json; charset=utf-8"
        }
        response = requests.post(url, data=json_data, headers=headers)
        
        if response.status_code == 200:
            print("POST请求成功！")
        else:
            print(f"POST请求失败，状态码：{response.status_code}")
            print("响应内容：", response.text)
    
    except requests.RequestException as e:
        print(f"请求错误: {e}")
    except ValueError:
        print("无法解析 JSON 数据")

data = {
    "body": "Test Bark Server",
    "title": "Test Title",
    "badge": 1,
    "category": "myNotificationCategory",
    "sound": "minuet.caf",
    "icon": "https://day.app/assets/images/avatar.jpg",
    "group": "test",
    "url": "https://mritd.com"
}

push_ios_notification(BARK_API, data)