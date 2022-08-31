import os
import pickle
from datetime import datetime

import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


class LinRegModel:
    '''
    Treinamento do modelo de Regressão Linear no dataset California Housing.

    Features utilizadas:
        - house_age
    '''
    
    def __init__(self, SEED = 123):
        self.SEED = SEED


    def train_model(self):
        '''
        Pipeline de treinamento do modelo
        '''
        print('Training model...')
        X_train, X_test, y_train, y_test = self.load_data()
        self.fit(X_train, y_train)
        print('Done!')
        self.evaluate(X_test, y_test)
        self.save()

        return self


    def load_data(self):
        '''
        Carrega e prepara os dados para treinamento
        '''
        X, y = fetch_california_housing(return_X_y = True, as_frame=True)
        data = pd.concat([X,y], axis=1)[['HouseAge', 'MedHouseVal']]
        data.columns = ['house_age', 'target']
        
        X_train, X_test, y_train, y_test = train_test_split(data['house_age'], data['target'], test_size=0.33, random_state=self.SEED)

        return X_train, X_test, y_train, y_test


    def fit(self, X_train, y_train):
        '''
        Fit do modelo
        '''
        scaler = StandardScaler()
        ln = LinearRegression()
        self.model = Pipeline([('scaler', scaler),('estimator', ln)])
        self.model.fit(X_train.to_numpy().reshape(-1, 1), y_train.to_numpy())
        
        return self.model


    def evaluate(self, X_test, y_test):
        '''
        Print MSE
        '''
        error = mean_squared_error(self.model.predict(X_test.to_numpy().reshape(-1,1)), y_test)
        print(f'MSE: {error:.3f}')


    def save(self, filename = None):
        '''
        Save model as pkl file.
        '''
        if filename is None:
            if not os.path.exists('src/training/temp'):
                os.mkdir('src/training/temp')
            filename = f'src/training/temp/ln-calhous-{str(datetime.today())}.pkl'.replace(' ','_')

        with open(filename,'wb') as file:
            pickle.dump(self.model,file)

    
        
            


if __name__ == '__main__':
    lnmodel = LinRegModel().train_model()


