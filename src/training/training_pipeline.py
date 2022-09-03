from infrastructure import S3Manager
from train import LinRegModel
import os


ARTIFACT_BUCKET_NAME = os.getenv('ARTIFACT_BUCKET_NAME')

# Cria bucket se não existe
s3_manager = S3Manager(ARTIFACT_BUCKET_NAME)
s3_manager.create()

# Treina modelo e salva artefato em diretório local
lnmodel = LinRegModel().train_model()

# Sobe modelo para o bucket
s3_manager.upload_file('src/training/temp')
