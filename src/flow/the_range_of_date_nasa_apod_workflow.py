import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from prefect import flow
from prefect import get_client
from task.the_range_of_date_crawler_data import the_range_of_date_crawler_data
from task.upload_to_gcs import upload_to_gcs
from prefect_github.repository import GitHubRepository
from task.read_api_key import read_api_key
from prefect.blocks.system import Secret

@flow
def range_nasa_apod_workflow(start_date, end_date, bucket_name):
    api_key = read_api_key()
    json_file_name = the_range_of_date_crawler_data(api_key, start_date, end_date)
    upload_to_gcs(json_file_name, bucket_name)

def deploy_flow():
    client = get_client()
    flow = range_nasa_apod_workflow.from_source(
        source=GitHubRepository.load("prefect"),
        entrypoint="src/flow/the_range_of_date_nasa_apod_workflow.py:range_nasa_apod_workflow",
    )

    flow.deploy(
        name="docker-deploy",
        tags=["test", "prefect"],
        work_pool_name="docker",
        job_variables=dict(pull_policy="Never"),
        parameters=dict(
            start_date="2024-08-18",
            end_date="2024-08-20",
            bucket_name='tir102_apod'
        ),
        cron="*/10 * * * *"
    )

if __name__ == "__main__":
    deploy_flow()

    start_date = "2024-08-18"
    end_date = "2024-08-20"
    bucket_name = 'tir102_apod'
    range_nasa_apod_workflow(start_date, end_date, bucket_name)
