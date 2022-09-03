import logging
import os
from datetime import datetime

import awswrangler as wr
import pandas as pd

from helper_functions import ModelLoaderS3

# Get configs
INPUT_FILE = os.getenv('INPUT_FILE','data.parquet')
STRATEGY = os.getenv('STRATEGY','latest')
ARTIFACT_BUCKET_NAME = os.getenv('ARTIFACT_BUCKET_NAME')
INFERENCE_BUCKET_NAME = os.getenv('INFERENCE_BUCKET_NAME')
S3_ENDPOINT = os.getenv('S3_ENDPOINT')


# Check whether it is a test execution
if S3_ENDPOINT is not None:
    wr.config.s3_endpoint_url = S3_ENDPOINT
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logging.info('Bucket de artefatos:', ARTIFACT_BUCKET_NAME)
logging.info('Bucket de inferencia:', INFERENCE_BUCKET_NAME)



def lambda_handler(event, context):

    # Carrega dados de input
    print(INPUT_FILE)
    input_data = wr.s3.read_parquet('s3://' + INFERENCE_BUCKET_NAME + '/' + INPUT_FILE)
    logging.info('Dados de input carregados com sucesso')


    # Carrega modelo e faz predicoes
    model, model_id = ModelLoaderS3(ARTIFACT_BUCKET_NAME).get_model(strategy = STRATEGY)
    preds = model.predict(input_data.to_numpy().reshape(-1,1))
    logging.info('Predicoes realizadas com sucesso')


    # Monta dataframe de output e escreve no s3
    output_data = pd.DataFrame()
    output_data['id'] = input_data.index
    output_data['preds'] = preds
    output_data['model_id'] = model_id
    output_data['pred_date'] = datetime.today().date()
    output_data['input_file'] = INPUT_FILE

    wr.s3.to_parquet(
                df=output_data,
                dataset=True,
                path='s3://' + INFERENCE_BUCKET_NAME + '/predicoes',
                mode="append"
        )
    logging.info('Predicoes salvas com sucesso')
    logging.info(output_data.head(3))

    return {
            'statusCode': 200
        }
