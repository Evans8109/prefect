import pandas as pd
from prefect import task
from task.google_cnl_api import google_cnl_api
from google.cloud import translate_v2 as translate

def process_tags(file_path):
    df = pd.read_json(file_path)
    
    # 确保我们处理的是所有行
    all_tags = []
    all_translations = []
    
    for _, row in df.iterrows():
        content_string = row['explanation']
        tags_list = google_cnl_api(content_string)
        
        # 初始化翻译客户端
        translate_client = translate.Client()
        
        # 翻译结果列表
        translated_array = []
        
        # 将英文翻译成中文
        for text in tags_list:
            result = translate_client.translate(text, target_language='zh-TW')
            translated_array.append(result['translatedText'])
        
        all_tags.extend(tags_list)
        all_translations.extend(translated_array)
    
    # 创建标签的 DataFrame
    df_tags = pd.DataFrame({
        'date': df['date'].repeat(len(all_tags) // len(df)),
        'tags_en': all_tags,
        'tags_zhTW': all_translations
    })
    
    # 创建标签的 DataFrame
    df_tags = pd.DataFrame({
        'date': df['date'].repeat(len(all_tags) // len(df)),
        'tags_en': all_tags,
        'tags_zhTW': all_translations
    })
    
    # 添加 Row 列
    df_tags = df_tags.reset_index(drop=True)
    df_tags.insert(0, 'Row', range(1, len(df_tags) + 1))
    
    return df_tags