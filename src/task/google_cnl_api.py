import statistics
import requests
import json
from prefect import task
from prefect.blocks.system import Secret

@task
def google_cnl_api(content_string):
    # 定義請求的 URL 和 API 金鑰
    secret_block = Secret.load("google-cnl-api-key")
    api_key = secret_block.get()
    url = f"https://language.googleapis.com/v1/documents:analyzeEntities?key={api_key}"
    # 定義請求的標頭和數據
    headers = {"Content-Type": "application/json"}
    data = {"document": {"type": "PLAIN_TEXT", "content": content_string}}

    # 發送 POST 請求
    response = requests.post(url, headers=headers, json=data)
    # 確保請求成功
    response.raise_for_status()
    # 將響應內容存儲到變數
    response_data = response.json()
    #print(json.dumps(response_data, indent=2))
    # 如果需要使用響應內容，可以在這裡進行處理
    salience_values = []
    entities = response_data.get("entities", [])
    for entity in entities:
        salience_values.append(entity.get("salience", None))
    # 計算中位數
    median_salience = statistics.median(salience_values)
    #print(median_salience)
    num_of_tags = 0
    entity_names = []

    for entity in entities:
        salience = entity.get("salience",0)
        # 比較 salience 是否大於 median_salience
        
        if salience > median_salience:
            num_of_tags += 1
            entity_names.append(entity["name"])
            # print(f'Entity: {entity["name"]}')
            # print(f'Salience: {salience}')
    #print("-------------------------------")
    #print(num_of_tags)
    #print([entity_names])
    tags_list = [entity_names]
    return tags_list