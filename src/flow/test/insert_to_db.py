import os
import json
import mysql.connector
from prefect import task
from prefect import flow

@task
def insert_to_db(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # 提取 date 和 title
    record = data[0]
    date = record.get('date')
    title = record.get('title')
    
    # 連接到 MySQL 資料庫
    conn = mysql.connector.connect(
        host='35.236.188.145',
        user='evans',
        password='123456',
        database='prefect'
    )
    cursor = conn.cursor()
    
    # 確保表存在
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prefect (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date VARCHAR(255),
        title VARCHAR(255)
    )
    ''')
    
    # 將 date 和 title 插入表中
    cursor.execute('''
    INSERT INTO prefect (date, title) VALUES (%s, %s)
    ''', (date, title))
    
    # 提交交易並關閉連接
    conn.commit()
    cursor.close()
    conn.close()


@flow
def my_flow():
    add_to_db("/Users/evans/Desktop/my_git/prefect/src/crawler_data/apod_data_2024-08-21.json")

# 如果你想要直接運行 flow
if __name__ == "__main__":
    my_flow()


#insert_to_db('src/crawler_data/apod_data_2024-08-21.json')