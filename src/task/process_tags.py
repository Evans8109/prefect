#pip install google-cloud-translate
import pandas as pd
from prefect import task
from task.google_cnl_api import google_cnl_api
from google.cloud import translate_v2 as translate

@task
def process_tags(file_path):

    df = pd.read_json(file_path)
    content_string = ' '.join(df['explanation'])
    tags_list = google_cnl_api(content_string)
    return tags_list