import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from prefect import flow
from task.crawler_data import crawler_data
from task.upload_to_gcs import upload_to_gcs
from prefect_github.repository import GitHubRepository

@flow
def nasa_apod_workflow(api_key, start_date, end_date, bucket_name):
    json_file_name = crawler_data(api_key, start_date, end_date)
    upload_to_gcs(json_file_name, bucket_name)

if __name__ == "__main__":
    with open('/workspaces/prefect/src/apikey.txt', 'r') as file:
        api_key = file.read().strip()

    nasa_apod_workflow.from_source(
        source=GitHubRepository.load("prefect"),
        entrypoint="src/flow/nasa_apod_workflow.py:nasa_apod_workflow",
    ).deploy(
        name="docker-deploy",
        tags=["test", "prefect"],
        work_pool_name="docker",
        job_variables=dict(pull_policy="Never"),
        # parameters=dict(name="Marvin"),
        cron="*/5 * * * *"
    )
    start_date = "2024-08-17"
    end_date = "2024-08-17"
    bucket_name = 'tir102_apod'

    nasa_apod_workflow(api_key, start_date, end_date, bucket_name)