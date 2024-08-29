import os
import json
import pandas as pd
from google.cloud import bigquery
from prefect import task
from google.oauth2 import service_account
from prefect.blocks.system import Secret

@task
def insert_to_tag(df_tags: pd.DataFrame, table_id: str = "my-project-tir102-bigquery.tir102_apod.tags", column_mapping: dict = None):
    """
    將 DataFrame 匯入 BigQuery 的指定表格，支持欄位映射。
    :param df_tags: 要匯入的 DataFrame
    :param table_id: 目標 BigQuery 表格 ID
    :param column_mapping: 欄位映射字典，將 DataFrame 欄位映射到 BigQuery 欄位 (選擇性)
    """
    # 從 Prefect 的 Secrets 管理服務中加載 BigQuery 憑證
    secret_block = Secret.load("bigquery-pord")
    credentials_dict = json.loads(secret_block.get())
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)

    # 建立 BigQuery 客戶端
    client = bigquery.Client(credentials=credentials)

    # 如果有欄位映射，則重命名 DataFrame 欄位
    if column_mapping:
        df_tags = df_tags.rename(columns=column_mapping)

    # 確保 DataFrame 中的欄位與 BigQuery 表格的欄位匹配
    table_schema = client.get_table(table_id).schema
    table_columns = [field.name for field in table_schema]
    df_tags = df_tags[[col for col in df_tags.columns if col in table_columns]]

    # 將 DataFrame 資料匯入 BigQuery
    df_tags.to_gbq(destination_table=table_id, project_id="my-project-tir102-bigquery", if_exists='append', credentials=credentials)
    
    print(f"Data successfully inserted into BigQuery table {table_id}.")