import requests
import json
import os
import easyocr
from datetime import datetime
from PIL import Image
from io import BytesIO


reader = easyocr.Reader(['ch_sim', 'en'])
BARK_API = os.environ.get("BARK_API")


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

def get_date_url():
    # Get current date
    d = datetime.now()
    y = d.year
    m = f"{d.month:02d}"  # Format month with leading zero if needed
    n = f"{d.day:02d}"    # Format day with leading zero if needed

    # Construct the URL
    url = f"https://img.owspace.com/Public/uploads/Download/{y}/{m}{n}.jpg"
    return url


def crop_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:

        with open("image.jpg", "wb") as f:
            f.write(response.content)

        image = Image.open("image.jpg")

        width, height = image.size

        # The first section includes the day and the lunar date.
        first_section = (0, 0, width, int(height * 0.15))

        # The second section includes the phrase "宜"
        second_section = (int(width * 0.2), int(height * 0.25), width - int(width * 0.2), int(height * 0.55))

        # The third section includes the article excerpt and the author information.
        third_section = (0, int(height * 0.55), width, height - int(height * 0.1))


        # Crop the image into the three specified sections
        first_img = image.crop(first_section)
        second_img = image.crop(second_section)
        third_img = image.crop(third_section)
        
        return first_img, second_img, third_img

        print("image has been croped according to the requirement")
    else:
        print("Cannot download image")
        return None, None, None

def ocr(image):
    try:
        # Convert the image to bytes
        image_bytes = BytesIO()
        image.save(image_bytes, format="JPEG")
        image_bytes = image_bytes.getvalue()

        # Perform OCR on the image bytes
        result = reader.readtext(image_bytes, detail=0)
        print("OCR Result:", result)
        return result
    except Exception as e:
        print("OCR error:", e)
        return None


def generate_data(date_list, recommendation_list, quote_list, url):
    date_string = '\n'.join(date_list)
    recommendation_string = next((item for item in recommendation_list if item.startswith('宜') or item.startswith('忌')), None)
    quote_string = ' '.join(quote_list[:-1])
    data = {
        "body": date_string + '\n' + '\n' + quote_string,
        "title": recommendation_string,
        "category": "myNotificationCategory",
        "icon": "https://github.com/MarkRushB/myDailyPush/blob/main/cal.png?raw=true",
        "group": "calendar",
        "url": url
    }
    return data

def do_it():
    try:
        print(BARK_API)
        url = get_date_url()
        first_section_img, second_section_img, third_section_img = crop_image(url)

        if first_section_img:
            date_list = ocr(first_section_img)
        if second_section_img:
            recommendation_list = ocr(second_section_img)
        if third_section_img:
            quote_list = ocr(third_section_img)

        push_payload = generate_data(date_list, recommendation_list, quote_list, url)
        
        push_ios_notification(BARK_API, push_payload)

    except Exception as e:
        print(f"An error occurred: {e}")


do_it()
