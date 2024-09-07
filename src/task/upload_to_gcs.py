from prefect import task
from google.cloud import storage
from google.oauth2 import service_account
from prefect.blocks.system import Secret
import json
import requests
import os

@task
def upload_to_gcs(json_file_name, bucket_name):
    
    secret_block = Secret.load("gcs-key")
    service_account_json = secret_block.get()
    
    # 解析 JSON 為字典
    credentials_dict = json.loads(service_account_json)
    print(type(service_account_json))
    
    # 創建服務帳戶憑證
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)
    
    # 創建 gcp 客户端
    storage_client = storage.Client(credentials=credentials)

    #定義路徑
    directory = "src/crawler_data"
    file_path = os.path.join(directory, json_file_name)
    
    # 讀取內容
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # 獲取bucket
    bucket = storage_client.bucket(bucket_name)

    for item in data:
        url = item['url']
        filename = f"{item['date']}"
        media_type = item['media_type']

        if media_type == 'video':
            filename += '.txt'
            content = f"Video URL: {url}"
            mime_type = 'text/plain'
        elif media_type == 'image':
            try:
                res = requests.get(url)
                content = res.content
                filename += '.jpg'
                mime_type = 'image/jpeg'

                if res.status_code != 200:
                    raise Exception(f"Failed to download content from URL: {url}")

            except Exception as e:
                print(f"Failed to handle URL {url}: {e}")
                continue

        blob = bucket.blob(filename)

        try:
            blob.upload_from_string(content, content_type=mime_type)
            print(f"File uploaded to {filename} in bucket {bucket_name}.")
        except Exception as e:
            print(f"Failed to upload {filename} to bucket {bucket_name}: {e}")