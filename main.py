import requests
import random
import string
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import os

load_dotenv(".env")

def generate_client_token():
    return "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(40))

def generate_access_token():
    print("[SYSTEM] Generating AccessToken")
    data = {
        "guid": os.getenv('EMAIL'),
        "password": os.getenv('PASSWORD'),
        "clientToken": generate_client_token(),
        "game_net": "Unity",
        "play_platform": "Unity",
        "game_net_user_id": ""
    }
    try:
        url = "https://www.realmofthemadgod.com/account/verify"
        verify_request = requests.post(url, data=data, headers=headers)
        access_token = ET.fromstring(verify_request.content).find(".//AccessToken").text
        if access_token:
            print(f"[SUCCESS] AccessToken: {access_token}")
            return access_token
    except Exception as e:
        print(f"[FAILURE] Failed to load calendar - {e}")

def load_character_list(access_token):
    data = {
        "doLogin": "true",
        "accessToken": access_token,
        "game_net": "Unity",
        "play_platform": "Unity",
        "game_net_user_id": ""
    }
    try:
        url = "https://www.realmofthemadgod.com/char/list"
        char_list_request = requests.post(url, data=data, headers=headers)
        username = ET.fromstring(char_list_request.content).find(".//Name").text
        if username:
            print(f"[SUCCESS] Username: {username} successfully logged in")
    except Exception as e:
        print(f"[FAILURE] Failed to load calendar - {e}")

def fetch_calendar(access_token):
    print("[SYSTEM] Fetching Daily Login Calendar")
    data = {
        "accessToken": access_token,
        "game_net": "Unity",
        "play_platform": "Unity",
        "game_net_user_id": ""
    }
    try:
        url = "https://www.realmofthemadgod.com/dailyLogin/fetchCalendar"
        fetch_calendar_request = requests.post(url, data=data, headers=headers)
        daily_login_data = fetch_calendar_request.content
        unlocked_days = ET.fromstring(daily_login_data).find("./Unlockable").get("days")
        consecutive_days = ET.fromstring(daily_login_data).find("./Consecutive").get("days")
        if unlocked_days and consecutive_days:
            print(f"[SUCCESS] Unlocked daily logins: {unlocked_days}")
            print(f"[SUCCESS] Consecutive daily logins: {consecutive_days}")
    except Exception as e:
        print(f"[FAILURE] Failed to load calendar - {e}")
    

if __name__ == "__main__":
    headers = {
        "User-Agent": "UnityPlayer/2021.3.5f1 (UnityWebRequest/1.0, libcurl/7.80.0-DEV)",
        "Accept": "*/*",
        "Accept-Encoding": "deflate, gzip",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Unity-Version": "2021.3.5f1"
    }

    access_token = generate_access_token()

    load_character_list(access_token)

    if access_token:
        fetch_calendar(access_token)