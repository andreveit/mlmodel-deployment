import logging
import pickle
import tempfile
from abc import ABC, abstractmethod

import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def remove_pref_suf(s):
    return '/'.join([i for i in s.split('/') if i != ""])


class FilesLister:
    '''
    List files in a given s3 key.
    '''
    def __init__(self, bucket: str, s3_client = None):
        self.bucket = bucket
        if s3_client is None:
            s3_client = boto3.client('s3')
        self.s3_client = s3_client


    def _retrieve_objects(self):
        '''
        Get all objects from S3.
        '''
        return self.s3_client.list_objects(Bucket = self.bucket)
    

    def _select_keys(self, keys_list, s3_key):
        '''
        Get objects that are inside th s3_key.
        '''
        selected_keys = []
        for key in keys_list:
            match_counter = 0
            for pat in s3_key.split('/'):
                if pat in key.split('/'):
                    match_counter += 1
                    
            if match_counter >= len(s3_key.split('/')):
                selected_keys.append(key)
    
        return selected_keys
    
    
    def list_files(self, s3_key: str):
        '''
        Returns a list of files in the selected key
        '''
        objects = self._retrieve_objects()
        s3_key = remove_pref_suf(s3_key)
        keys_list = [ i['Key'] for i in objects['Contents'] ]
        
        if s3_key in ['','/','.']:
            return keys_list
        return self._select_keys(keys_list,s3_key)



class ModelSelectorBase(ABC):
    '''
    Base class for Model selection Strategy
    '''
    @abstractmethod
    def select(self):
        pass


class ModelSelectorLatest(ModelSelectorBase):
    '''
    Selects the latest model
    '''
    def select(self, models_list: list) -> str:
        models_list.sort()
        return models_list[-1]


class ModelLoaderBase(ABC):
    '''
    Classe base para carregar modelo para inferencia.
    '''
    # Dicionario para selecao da estrategia
    strategy_dict = {
        'latest': ModelSelectorLatest
    }

    @abstractmethod
    def get_model(self):
        pass


class ModelLoaderS3(ModelLoaderBase):
    '''
    Carrega modelo do bucket de artefatos
    '''
    def __init__(self, bucket):
        self.bucket = bucket
        self.s3_client = boto3.client('s3')


    def get_model(self, strategy: str = 'latest'):
        '''
        Retorna objeto do modelo e indentificacao
        '''
        model_key = self.select_model(strategy)
        return self._get_model(model_key), model_key


    def _get_model(self, model_key: str):
        '''
        Retorna modelo carregado do S3 (objeto)
        '''
        with tempfile.TemporaryFile(mode='w+b') as fp:
            self.s3_client.download_fileobj(Fileobj=fp,Bucket=self.bucket, Key=model_key)
            fp.seek(0)
            return pickle.load(fp)


    def select_model(self, strategy: str) -> str:
        '''
        Seleciona o modelo eleito de uma lista
        de acordo com a estrategia selecionada
        '''
        models_list = FilesLister(self.bucket, self.s3_client).list_files('/')
        model_key =  self.strategy_dict[strategy]().select(models_list)
        logging.info(f'Modelo selecionado: {model_key}, Estrategia: "{strategy}"')
        return model_key
