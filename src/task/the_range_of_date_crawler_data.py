from prefect import task
import requests
import json
from datetime import datetime
import os

@task
def the_range_of_date_crawler_data(api_key, start_date, end_date):
    base_url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": api_key}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        # Define the directory and file path
        directory = "src/crawler_data"
        # check the directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)
        file_name = f'apod_data_{start_date}_{end_date}.json'
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)
        print(f"資料已儲存為 {file_name}")
        return file_name
    else:
        raise Exception(f"Error fetching data: {response.status_code} - {response.text}")