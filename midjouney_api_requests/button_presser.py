import requests
from dotenv import load_dotenv
import os

load_dotenv()

apiUrl = os.getenv("API_URL")
token = os.getenv("API_TOKEN")


def press_button(jobid, button):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    body = {
        "jobid": f"{jobid}",
        "button": f"{button}"
    }
    response = requests.post(apiUrl, headers=headers, json=body)
    return response.json()


def press_u1_button(jobid):
    return press_button(jobid, "U1")


def press_u2_button(jobid):
    return press_button(jobid, "U2")


def press_u3_button(jobid):
    return press_button(jobid, "U3")


def press_u4_button(jobid):
    return press_button(jobid, "U4")


def press_upscale_button(jobid):
    return press_button(jobid, "Upscale (Subtle)")
