from prefect import task
from prefect.blocks.system import Secret

@task
def read_api_key():
    secret_block = Secret.load("api-key")
    return secret_block.get()