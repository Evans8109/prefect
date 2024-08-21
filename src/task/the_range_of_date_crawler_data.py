from prefect import task
import requests
import json

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
        file_name = f'apod_data_{start_date}_{end_date}.json'
        with open(file_name, 'w') as json_file:
            json.dump(data, json_file, indent=2)
        print(f"資料已儲存為 {file_name}")
        return file_name
    else:
        raise Exception(f"Error fetching data: {response.status_code} - {response.text}")