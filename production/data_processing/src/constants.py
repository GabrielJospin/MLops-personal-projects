import os

BUCKET = os.environ.get('BUCKET')
PROCESS = ['purchasing']
S3_KEY = os.environ.get("S3_KEY")
S3_SECRET = os.environ.get("S3_SECRET")


def get_data_path(processing):
    return f'dl/data-processing/{processing}/data'


def get_out_path(processing, job_execution_id, name):
    return f'dl/data-processing/{processing}/out/{job_execution_id}/{name}'


def get_archive_path(processing, job_execution_id, name):
    return f'dl/data-processing/{processing}/archive/{job_execution_id}/{name}'


def get_meta_path(processing):
    return f'dl/data-processing/{processing}/meta/config.json'
