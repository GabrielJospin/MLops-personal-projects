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
            landed_files = self.filter_files(data_processing_bucket, get_path(proc))
            for landed_file in landed_files:
                landed_files_by_type[proc].append(landed_file)
                self.logger.info(f'Landed s3://{landed_file.bucket_name}/{landed_file.key}')

        return landed_files_by_type
