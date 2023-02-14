import json

import boto3
import ulid as ulid
from Logger import Logger
from constants import *
from FileManager import FileManager
from DataframeManager import DataframeManager

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')


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
    dataframe_manager = DataframeManager()

    logger.info('start processing')
    logger.info(f'execution id={job_execution_id}')
    landed_files_by_type = file_manager.find_landed_files()
    logger.info(f'landed {len(landed_files_by_type)} file(s)')
    process_files = dataframe_manager.process_landed_files(landed_files_by_type, job_execution_id, file_manager)
    return results(200, job_execution_id, process_files, [])


if __name__ == '__main__':
    main(None, None)
