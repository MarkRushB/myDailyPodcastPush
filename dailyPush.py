import requests

def fetch_and_parse_json(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"请求错误: {e}")
    except ValueError:
        print("无法解析 JSON 数据")


url = "https://xyzrank.com/assets/hot-episodes.24ef12b57741554e245e301ea9240f8f.json"


data = fetch_and_parse_json(url)
print(data)
