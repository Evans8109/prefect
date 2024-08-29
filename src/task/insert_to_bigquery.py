import os
import json
from google.cloud import bigquery
from google.oauth2 import service_account
from prefect.blocks.system import Secret
from prefect import task

@task
def insert_to_bigquery(file_path):
    try:
        # 讀取文件
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # 從 JSON 中提取數據
        record = data[0]
        date = record.get('date')
        media_type = record.get('media_type')
        title = record.get('title')
        url = record.get('url')
        copyright = record.get('copyright')

#        if tags_list and isinstance(tags_list, list) and len(tags_list) > 0:
#            tags_list = tags_list[0]  # 取出內部列表
#        else:
#            tags_list = []
        
        secret_block = Secret.load("bigquery-pord")
        secret_block = secret_block.get()
        credentials_dict = json.loads(secret_block)
        credentials = service_account.Credentials.from_service_account_info(credentials_dict)

        # 建立 BigQuery 客戶端
        client = bigquery.Client(credentials=credentials)
        # 指定 BigQuery 表格 ID
        table_id = "my-project-tir102-bigquery.tir102_apod.apod"  # 使用正確的資料集名稱

        # 準備要插入的行
        rows_to_insert = [
            {
                u"date": date, 
                u"title": title, 
#                u"explanation": tags_list, 
                u"media_type": media_type,
                u"URL": url,
                u"copyright": copyright
            }
        ]

        # 插入數據到 BigQuery
        errors = client.insert_rows_json(table_id, rows_to_insert)
        if errors == []:
            print("新行已添加到 BigQuery。")
        else:
            print(f"插入行時遇到錯誤: {errors}")
    
    except FileNotFoundError as e:
        print(f"文件未找到: {e}")
    
    except json.JSONDecodeError as e:
        print(f"JSON 格式錯誤: {e}")
    
    except Exception as e:  # 捕捉所有異常
        print(f"發生錯誤: {e}")
