import json

import boto3
import ulid as ulid
from Logger import Logger
from constants import *
from FileManager import FileManager

s3 = boto3.resource('s3')
s3_client = boto3.client('s3',
                         aws_access_key_id=S3_KEY,
                         aws_secret_access_key=S3_SECRET)


def results(status, job_execution_id, processed, failed):
    return {
        'statusCode': status,
        'body': json.dumps({
            'job_execution_id': job_execution_id,
            'processed_files': [f's3://{f.bucket_name}/{f.key}' for f in processed],
            'failed_files': [f's3://{f.bucket_name}/{f.key}' for f in failed]
        })
    }


def main(event, context):
    logger = Logger(__name__)
    job_execution_id = ulid.ulid()
    file_manager = FileManager(s3, s3_client)
    logger.info('start processing')
    logger.info(f'execution id={job_execution_id}')
    landed_files_by_type = file_manager.find_landed_files()
    pass


if __name__ == '__main__':
    main(None, None)
