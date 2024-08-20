from prefect import task
from google.cloud import storage
from google.oauth2 import service_account
from prefect.blocks.system import Secret
import json
import requests
import mimetypes
import re

@task
def upload_to_gcs(json_file_name, bucket_name):
    # 从 Prefect Secret 中加载服务账户凭证 JSON 字符串
    secret_block = Secret.load("gcs-key")
    service_account_json = secret_block.get()  # 获取 Secret 的值
    
    # 解析 JSON 字符串为字典
    credentials_dict = json.loads(service_account_json)
    
    # 创建服务账户凭证对象
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)
    
    # 创建 Google Cloud Storage 客户端
    storage_client = storage.Client(credentials=credentials)
    
    # 读取要上传的文件内容
    with open(json_file_name, 'r') as file:
        data = json.load(file)
    
    # 获取目标 Bucket
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
