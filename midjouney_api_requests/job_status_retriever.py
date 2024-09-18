from datetime import datetime
from dotenv import load_dotenv
import os
import requests
import time

load_dotenv()

apiUrl = os.getenv("API_URL")
token = os.getenv("API_TOKEN")


def fetch_job_details(job_id):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    try:
        response = requests.get(apiUrl, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("Fehler:", response.status_code)
    except Exception as e:
        print("Ein Fehler ist aufgetreten:", e)


def check_image_status(job_id):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        response = requests.get(apiUrl, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"{datetime.now()}: Fehler beim Abrufen des Status:", response.status_code)
            return None
    except Exception as e:
        print(f"{datetime.now()}: Ein Fehler ist aufgetreten:", e)
        return None


def wait_for_image_completion(job_id):
    start_time = time.time()
    timeout = 600  # 10 Minuten

    while True:
        current_time = time.time()
        if current_time - start_time > timeout:
            print(f"{datetime.now()}: Maximale Wartezeit überschritten, Abbruch.")
            break

        status_response = check_image_status(job_id)
        if status_response is None:
            print(f"{datetime.now()}: Abbruch wegen eines Fehlers.")
            break
        elif status_response['status'] == 'completed':
            print(f"{datetime.now()}: Bildgenerierung abgeschlossen.")
            break
        elif status_response['status'] != 'failed':
            print(f"{datetime.now()}: Bildgenerierung noch nicht abgeschlossen, warte 10 Sekunden...")
            time.sleep(10)  # Warte für 10 Sekunden vor dem nächsten Status-Check
        else:
            print(f"{datetime.now()}: Unbekannter Status: {status_response['status']}")
            break

