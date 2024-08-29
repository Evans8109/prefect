import pandas as pd
from prefect import task
from task.google_cnl_api import google_cnl_api
from google.cloud import translate_v2 as translate

@task
def process_tags(file_path):

    df = pd.read_json(file_path)
    fig_date = df['date']
    content_string = ' '.join(df['explanation'])
    tags_list = google_cnl_api(content_string)

    # 初始化翻譯客戶端
    translate_client = translate.Client()
    # 翻譯結果列表
    translated_array = []
    # 將英文翻譯成中文
    for text in tags_list:
        result = translate_client.translate(text, target_language='zh-TW')
#        print(result)
        translated_array.append(result['translatedText'])


    #創造tags的dataframe
    df_tags=pd.DataFrame({
        'tags_en' : tags_list,
        'tags_zhTW' : translated_array 
    })

    # 在 DataFrame 最前面插入一個 date 欄位，值為 fig_date
    df_tags.insert(0, 'date', fig_date)
    # print(df_tags)

    return df_tags