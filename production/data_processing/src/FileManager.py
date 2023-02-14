import io
import json
from collections import defaultdict

from Logger import Logger
from constants import *


class FileManager:

    def __init__(self, s3, s3_client) -> None:
        super().__init__()
        self.logger = Logger(__name__)
        self.s3_client = s3_client
        self.s3 = s3

    @staticmethod
    def filter_files(bucket, prefix):
        return list(f for f in bucket.objects.filter(Prefix=prefix) if not f.key.endswith('/'))

    def find_landed_files(self):
        data_processing_bucket = self.s3.Bucket(BUCKET)
        landed_files_by_type = {
            'purchasing': list()
        }

        for proc in PROCESS:
            landed_files = self.filter_files(data_processing_bucket, get_data_path(proc))
            for landed_file in landed_files:
                landed_files_by_type[proc].append(landed_file)
                self.logger.info(f'Landed s3://{landed_file.bucket_name}/{landed_file.key}')

        return landed_files_by_type

    def open(self, path):
        data_processing_bucket = self.s3.Bucket(BUCKET)
        file = self.filter_files(data_processing_bucket, path)[0]
        return file

    def remove(self, path):
        data_processing_bucket = self.s3.Bucket(BUCKET)
        file = self.filter_files(data_processing_bucket, path)[0]
        file.delete()

    @staticmethod
    def save(df, path):
        real_path = f's3://{BUCKET}/{path}'
        df.to_csv(real_path, index=False)

    def move_to_archive(self, file, processing, job_execution_id):
        path = f's3://{file.bucket_name}/{file.key}'
        archive_path = f's3://{file.bucket_name}/{get_archive_path(processing, job_execution_id, file.key.split("/")[-1])}'
        self.logger.info(f'Coping {path} to {archive_path}')
        self.s3_client.copy({
            'Bucket': file.bucket_name,
            'Key': file.key
        }, file.bucket_name, f'{get_archive_path(processing, job_execution_id, file.key.split("/")[-1])}')
        return archive_path
