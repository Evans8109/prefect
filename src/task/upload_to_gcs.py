from prefect import task
from google.cloud import storage
from google.oauth2 import service_account
import json
import requests
import mimetypes
import re

@task
def upload_to_gcs(json_file_name, bucket_name):
    # 加载服务账户凭证
    credentials = service_account.Credentials.from_service_account_file(
        '/app/src/task/evans-class-c67887cf1aed.json'
    )
    storage_client = storage.Client(credentials=credentials)

    with open(json_file_name, 'r') as file:
        data = json.load(file)

    bucket = storage_client.bucket(bucket_name)

    for item in data:
        url = item['url']
        filename = f"{item['date']}"

        # 判断 URL 是否为 YouTube 链接
        if re.match(r'https://www\.youtube\.com/embed/', url):
            filename += '.txt'
            content = f"Video URL: {url}"
            mime_type = 'text/plain'
        else:
            try:
                res = requests.get(url)
                content = res.content
                mime_type, _ = mimetypes.guess_type(url)

                if mime_type and mime_type.startswith('video'):
                    filename += '.mp4'
                elif mime_type and mime_type.startswith('image'):
                    filename += '.jpg'
                else:
                    filename += '.bin'  # Default to .bin if MIME type is unknown

                # Check if the request was successful
                if res.status_code != 200:
                    raise Exception(f"Failed to download content from URL: {url}")

            except Exception as e:
                print(f"Failed to handle URL {url}: {e}")
                continue  # Skip this item if there's an error

        blob = bucket.blob(filename)
        
        try:
            blob.upload_from_string(content, content_type=mime_type or 'application/octet-stream')
            print(f"File uploaded to {filename} in bucket {bucket_name}.")
        except Exception as e:
            print(f"Failed to upload {filename} to bucket {bucket_name}: {e}")
