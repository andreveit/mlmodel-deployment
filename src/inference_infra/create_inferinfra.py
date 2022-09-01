import os
import sys

sys.path.append(os.path.abspath("./src"))
import pandas as pd
from training.infrastructure import S3Manager
from training.train import LinRegModel

from helper_functions import tempdir_context


TEMPFILE = 'data.pkl'

inferenct_bucket_name = os.getenv('INFERENCE_BUCKET_NAME')


# Cria bucket se não existe
s3_manager = S3Manager(inferenct_bucket_name)
s3_manager.create()


with tempdir_context('temp/') as tempdir:
    
    # Obtem os dados para inferencia
    lnmodel = LinRegModel()
    _, X_test, _, _ = lnmodel.load_data()
    X_test.to_pickle(tempdir + TEMPFILE)

    # Sobe dados de inferencia para o bucket
    s3_manager.upload_file(tempdir)
