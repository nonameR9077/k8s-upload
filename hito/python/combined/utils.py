from datetime import datetime
# date
def is_isoformat(s: str) -> bool:
    try:
        datetime.fromisoformat(s)
        return True
    except ValueError:
        return False

def date_to_isoformat(element):
    raw_date = element.get_attribute("data-posted")
    return datetime.fromisoformat(raw_date)


import json
from google.cloud import storage
# Google Cloud Storage(GCS)
def get_bucket_data(bucket_name, file_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    return json.loads(blob.download_as_text())

def save_bucket_data(bucket_name, file_name, data):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(json.dumps(data, indent=2))
    print("✅ Data uploaded to GCS.")


import requests
from constants import SLACK_WEBHOOK_URL
# slack
def send_slack_message(text):
    requests.post(SLACK_WEBHOOK_URL, json={"text": text})

def format_items(items, is_hito=True):
    text = ""
    for idx, item in items.items():
        text += (
            f"  {idx}:\n"
            f"    title: {item['title']}\n"
        )

        if is_hito:
            text += (
            f"    type: {item['type']}\n"
            f"    lang: {item['lang']}\n"
            )
        
        text += (    
            f"    date: {item['date']}\n"
            f"    url: {item['url']}\n\n"
        )
    return text
