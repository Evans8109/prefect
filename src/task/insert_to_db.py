import os
import json
import mysql.connector
from prefect import task

@task
def insert_to_db(file_path):
    try:
        # read file
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # from json extract data
        record = data[0]
        date = record.get('date')
        title = record.get('title')
        
        # connect to mysql
        conn = mysql.connector.connect(
            host='35.236.188.145',
            user='evans',
            password='123456',
            database='prefect'
        )
        cursor = conn.cursor()
        
        # 確認table 存在
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS prefect (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date VARCHAR(255),
            title VARCHAR(255)
        )
        ''')
        
        # data insert table
        cursor.execute('''
        INSERT INTO prefect (date, title) VALUES (%s, %s)
        ''', (date, title))
        
        # 提交交易
        conn.commit()
    
    except FileNotFoundError as e:
        print(f"文件未找到: {e}")
    
    except json.JSONDecodeError as e:
        print(f"JSON格式錯誤: {e}")
    
    except mysql.connector.Error as e:
        print(f"MySQL連線: {e}")
    
    except Exception as e:
        print(f"其他錯誤: {e}")
    
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass