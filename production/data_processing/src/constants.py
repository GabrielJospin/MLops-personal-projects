import os

BUCKET = os.environ.get('BUCKET')
PROCESS = ['purchasing']
S3_KEY = os.environ.get("S3_KEY")
S3_SECRET = os.environ.get("S3_SECRET")

def get_path(processing):
    return f'dl/data-processing/{processing}/data'
