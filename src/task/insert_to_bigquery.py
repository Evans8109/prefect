import os
import json
from google.cloud import bigquery
from prefect import task

@task
def insert_to_bigquery(file_path, tags_list):
    try:
        # 讀取文件
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # 從 JSON 中提取數據
        record = data[0]
        date = record.get('date')
        title = record.get('title')

        if tags_list and isinstance(tags_list, list) and len(tags_list) > 0:
            tags_list = tags_list[0]  # 取出內部列表
        else:
            tags_list = []

        # 建立 BigQuery 客戶端
        client = bigquery.Client()

        # 指定 BigQuery 表格 ID
        table_id = "evans-class.prefect.prefect" 

        # 準備要插入的行
        rows_to_insert = [
            {u"date": date, u"title": title, u"explanation": tags_list}
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
