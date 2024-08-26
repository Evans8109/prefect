from prefect import task
from prefect.blocks.system import Secret

# for gcs bucket 
@task
def read_api_key():
    secret_block = Secret.load("api-key")
    return secret_block.get()