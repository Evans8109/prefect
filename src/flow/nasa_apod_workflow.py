import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from prefect import flow
from datetime import datetime
from prefect import get_client
from task.crawler_data import crawler_data
from task.upload_to_gcs import upload_to_gcs
from prefect_github.repository import GitHubRepository
from task.read_api_key import read_api_key
from prefect.blocks.system import Secret

@flow
def nasa_apod_workflow(bucket_name):
    today = datetime.now().strftime('%Y-%m-%d')
    api_key = read_api_key()
    json_file_name = crawler_data(api_key, today, today)
    upload_to_gcs(json_file_name, bucket_name)

def deploy_flow():
    client = get_client()
    flow = nasa_apod_workflow.from_source(
        source=GitHubRepository.load("prefect"),
        entrypoint="src/flow/nasa_apod_workflow.py:nasa_apod_workflow",
    )

    flow.deploy(
        name="docker-deploy",
        tags=["test", "prefect"],
        work_pool_name="docker",
        job_variables=dict(pull_policy="Never"),
        parameters=dict(
            bucket_name='tir102_apod'
        ),
        cron="*/5 * * * *"
    )

if __name__ == "__main__":
    deploy_flow()

    bucket_name = 'tir102_apod'
    nasa_apod_workflow(bucket_name)