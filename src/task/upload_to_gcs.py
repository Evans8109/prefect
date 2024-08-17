# src/task/222.py
from prefect import task
import requests
import json
import mimetypes
from google.cloud import storage
from google.oauth2 import service_account

@task
def upload_to_gcs(json_file_name, bucket_name):
    # 加載服務帳戶憑證
    credentials = service_account.Credentials.from_service_account_file(
        '/workspaces/prefect/src/task/evans-class-c67887cf1aed.json'
    )
    storage_client = storage.Client(credentials=credentials)

    with open(json_file_name, 'r') as file:
        data = json.load(file)

    for item in data:
        res = requests.get(item['url'])
        content = res.content

        filename = f"{item['date']}.jpg"
        mime_type, _ = mimetypes.guess_type(filename)

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(filename)

        blob.upload_from_string(content, content_type=mime_type)
        print(f"File uploaded to {filename} in bucket {bucket_name}.")
