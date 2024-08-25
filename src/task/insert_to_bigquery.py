import os
import json
from google.cloud import bigquery
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
        title = record.get('title')
        
        # 建立 BigQuery 客戶端
        client = bigquery.Client()

        # 指定 BigQuery 表格 ID
        table_id = "evans-class.prefect.prefect"  # 修改為你的項目 ID 和資料集名稱

        # 準備要插入的行
        rows_to_insert = [
            {u"date": date, u"title": title}
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
    
    except bigquery.exceptions.GoogleCloudError as e:
        print(f"BigQuery 錯誤: {e}")
    
    except Exception as e:
        print(f"其他錯誤: {e}")

# 示例用法：
# insert_to_bigquery('xxx.json')
