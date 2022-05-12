import os.path

from qcloud_cos import CosConfig, CosS3Client


class CosPicUploader:
    def __init__(self, secret_id, secret_key, region, bucket):
        self.__bucket = bucket
        self.__config = CosConfig(Region=region, Secret_id=secret_id, Secret_key=secret_key)
        self.__client = CosS3Client(self.__config)

    def upload_file(self, key, file_path):
        file_path = file_path.replace('\\', '/')
        with open(file_path, 'rb') as f:
            self.__client.put_object(Bucket=self.__bucket, Body=f, Key=key)
            res = self.__client.get_object_url(Bucket=self.__bucket, Key=key)
            return res
