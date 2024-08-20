from prefect import task
@task
def read_api_key(file_path: str) -> str:
    with open(file_path, 'r') as file:
        api_key = file.read().strip()
    return api_key