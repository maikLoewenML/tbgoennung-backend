import requests
from dotenv import load_dotenv
import os

load_dotenv()

apiUrl = os.getenv("API_URL")
token = os.getenv("API_TOKEN")
discord = os.getenv("DISCORD_TOKEN")
server = os.getenv("SERVER")
channel = os.getenv("CHANNEL")


def send_prompt_to_api(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    body = {
        "prompt": prompt,
        "discord": discord,
        "server": server,
        "channel": channel
    }
    try:
        response = requests.post(apiUrl, headers=headers, json=body)
        return response.status_code, response.json().get("jobid")
    except Exception as e:
        print("Ein Fehler ist aufgetreten:", e)
        return None, None
