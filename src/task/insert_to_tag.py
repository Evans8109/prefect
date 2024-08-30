import os
import json
import pandas as pd
import pandas_gbq
from google.cloud import bigquery
from prefect import task
from google.oauth2 import service_account
from prefect.blocks.system import Secret

@task
def insert_to_tag(df_tags: pd.DataFrame, project_id: str, dataset_id: str, table_name: str):
    # 如果 'Row' 列存在且不需要，可以删除它
    if 'Row' in df_tags.columns:
        df_tags = df_tags.drop(columns=['Row'])

    # 将日期转换为字符串
    df_tags['date'] = pd.to_datetime(df_tags['date'])
    df_tags['date'] = df_tags['date'].astype(str)

    # 构建完整的表 ID
    table_id = f"{project_id}.{dataset_id}.{table_name}"
    
    # 从 Prefect 的 Secret 管理中加载 BigQuery 凭据
    secret_block = Secret.load("bigquery-pord")
    credentials_dict = json.loads(secret_block.get())
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)
    
    # 创建 BigQuery 客户端
    client = bigquery.Client(credentials=credentials, project=project_id)
    
    try:
        # 将数据加载到 BigQuery
        job = client.load_table_from_dataframe(df_tags, table_id)
        job.result()  # 等待作业完成

        print(f"Successfully inserted {job.output_rows} rows into BigQuery table {table_id}.")
    except Exception as e:
        print(f"Error inserting data: {str(e)}")
        raise
