import logging
import os

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)


class S3Manager:
    '''
    Classe responsável por gerenciar recursos no S3.

    AWS_ACCESS_KEY_ID e AWS_SECRET_ACCESS_KEY devem estar
    setadas como variáveis de ambiente.
    '''

    def __init__(self, bucket_name = 'models-artifactstore-andreveit'):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')


    def check_if_exists(self):
        '''
        Verifica se o bucket já foi criado na conta utilizada.
        '''
        bucket_list = self.s3_client.list_buckets()['Buckets']
        
        for bucket in bucket_list:
            if self.bucket_name == bucket['Name']:
                return True
        return False


    def _create(self):
        try:
            self.s3_client.create_bucket(Bucket=self.bucket_name)

        except ClientError as e:
            logging.error(e)
            return False
        return True


    def create(self):
        '''
        Cria bucket se não existir - Verifica se já não foi
        criado na conta utilizada.
        '''
        if not self.check_if_exists():
            if self._create():
                logging.info(f'Created bucket: {self.bucket_name}')
            return

        logging.info(f'Bucket already exists: {self.bucket_name}')



    def upload_file(self, file_name):
        """
        Upload file to S3 bucket
        """
        object_name = os.path.basename(file_name)

        try:
            response = self.s3_client.upload_file(file_name, self.bucket_name, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        logging.info(f'Model {object_name} was uploaded to S3.')
        return True
        

    def delete(self):
        self.s3_client.delete_bucket(Bucket=self.bucket_name)
