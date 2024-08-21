from prefect import task
import requests
import json
from datetime import datetime

@task
def crawler_data(api_key, start_date, end_date):
    base_url = "https://api.nasa.gov/planetary/apod"
    today = datetime.now().strftime('%Y-%m-%d')
    params = {
        "api_key": api_key,
        "start_date": today,
        "end_date": today
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        file_name = f'apod_data_{today}.json'
        with open(file_name, 'w') as json_file:
            json.dump(data, json_file, indent=2)
        print(f"資料已儲存為 {file_name}")
        return file_name
    else:
        raise Exception(f"Error fetching data: {response.status_code} - {response.text}")