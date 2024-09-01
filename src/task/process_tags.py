import pandas as pd
import json
from prefect import task
from task.google_cnl_api import google_cnl_api
from prefect.blocks.system import Secret
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account

@task
def process_tags(file_path):
    secret_block = Secret.load("new-cnl-api-key")
    service_account_json = secret_block.get()
    credentials_dict = json.loads(service_account_json)
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)
    df = pd.read_json(file_path)
    
    # 确保我们处理的是所有行
    all_tags = []
    all_translations = []
    all_dates = []

    # 初始化翻译客户端
    translate_client = translate.Client(credentials=credentials)

    for _, row in df.iterrows():
        content_string = row['explanation']
        tags_list = google_cnl_api(content_string)
        
        # 翻译结果列表
        translated_array = []
        
        # 将英文翻译成中文
        for text in tags_list:
            result = translate_client.translate(text, target_language='zh-TW')
            translated_array.append(result['translatedText'])
        
        # 将数据添加到列表中
        all_tags.extend(tags_list)
        all_translations.extend(translated_array)
        all_dates.extend([row['date']] * len(tags_list))
    
    # 创建标签的 DataFrame
    df_tags = pd.DataFrame({
        'date': all_dates,
        'tags_en': all_tags,
        'tags_ehTW': all_translations
    })

    # 添加 Row 列
    df_tags = df_tags.reset_index(drop=True)
    df_tags.insert(0, 'Row', range(1, len(df_tags) + 1))
    
    return df_tags