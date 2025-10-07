import requests
import json
import time
import re

def request_comments(post_id, cursor=0):
    url = f'https://www.tiktok.com/api/comment/list/?aid=1988&app_name=tiktok_web&aweme_id={post_id}&count=20&cursor={cursor}'
    
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'vi-VN,en-US;q=0.9,en;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'referer': 'https://www.tiktok.com/',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f" HTTP error {response.status_code}")
            return {}
        return response.json()
    except json.JSONDecodeError:
        print("token expired or blocked")
        print(response.text[:200])
        return {}
    except requests.RequestException as e:
        print(f"request failed: {e}")
        return {}

def parse_comments(data, comment_list):
    comments_data = data.get('comments', [])
    for cmt in comments_data:
        text = cmt.get('share_info', {}).get('desc', '')
        if not text:
            text = cmt.get('text', '')
        text = clean_text(text)
        if text:
            comment_list.append(text)
    return data.get('has_more', 0)

def clean_text(text):
    emoji = re.compile("["
        u"\U0001F600-\U0001F64F"  # Emoticons
        u"\U0001F300-\U0001F5FF"  # Symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # Transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # Flags
        u"\U00002702-\U000027B0"  # Dingbats
        u"\U000024C2-\U0001F251"  # Enclosed characters
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA70-\U0001FAFF"  # Symbols for new emoji
        u"\U00002500-\U00002BEF"  # Chinese symbols, boxes
        u"\u200d"                 # Zero width joiner
        u"\u2640-\u2642"          # Gender symbols
        u"\u2600-\u26FF"          # Misc symbols
        u"\u2300-\u23FF"          # Technical symbols
        "]+", flags=re.UNICODE)
    text = emoji.sub(r'', text)
    text = re.sub(r".*?[’']s comment:\s*", "", text, flags=re.IGNORECASE)
    text = ' '.join(text.split())
    return text

#

post_url = input("Nhập URL video TikTok: ")
post_id = post_url.split('/')[-1]

all_comments = []

cursor = 0
while True:
    data = request_comments(post_id, cursor)
    if not data:
        break
    has_more = parse_comments(data, all_comments)
    if has_more == 1:
        cursor += 20
        print(f"➡ Moving to next cursor: {cursor}")
        time.sleep(1)
    else:
        print("All comments fetched")
        break

with open('comments.json', 'w', encoding='utf-8') as f:
    json.dump(all_comments, f, ensure_ascii=False, indent=4)

print("Done")
