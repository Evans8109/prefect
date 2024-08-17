import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from prefect import flow
from task.crawler_data import crawler_data
from task.upload_to_gcs import upload_to_gcs

@flow
def nasa_apod_workflow(api_key, start_date, end_date, bucket_name):
    json_file_name = crawler_data(api_key, start_date, end_date)
    upload_to_gcs(json_file_name, bucket_name)

if __name__ == "__main__":
    with open('../apikey.txt', 'r') as file:
        api_key = file.read().strip()

    start_date = "2024-08-17"
    end_date = "2024-08-17"
    bucket_name = 'tir102_apod'

    nasa_apod_workflow(api_key, start_date, end_date, bucket_name)
