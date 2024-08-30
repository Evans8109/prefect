import os
import json
import pandas as pd
import pandas_gbq
from google.cloud import bigquery
from prefect import task
from google.oauth2 import service_account
from prefect.blocks.system import Secret

@task
def insert_to_tag(df_tags: pd.DataFrame, table_id: str = None, column_mapping: dict = None):

    # 預設值定義
    project_id = "my-project-tir102-bigquery"
    dataset_id = "tir102_apod"
    table_id = f"{project_id}.{dataset_id}.tag"
    
    if table_id is None:
        table_id = table_id

    # 從 Prefect 的 Secrets 管理服務中加載 BigQuery 憑證
    secret_block = Secret.load("bigquery-pord")
    credentials_dict = json.loads(secret_block.get())
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)

    # 建立 BigQuery 客戶端
    client = bigquery.Client(credentials=credentials, project=project_id)

    # 如果有欄位映射，則重命名 DataFrame 欄位
    if column_mapping:
        df_tags = df_tags.rename(columns=column_mapping)

    # 確保 DataFrame 中的欄位與 BigQuery 表格的欄位匹配
    table_schema = client.get_table(table_id).schema
    table_columns = [field.name for field in table_schema]
    df_tags = df_tags[[col for col in df_tags.columns if col in table_columns]]

    # 將 DataFrame 資料匯入 BigQuery
    pandas_gbq.to_gbq(df_tags, destination_table=table_id, project_id=project_id, if_exists='append', credentials=credentials)    
    print(f"Data successfully inserted into BigQuery table {table_id}.")