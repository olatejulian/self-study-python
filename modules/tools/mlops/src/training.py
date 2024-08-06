'''
Script para treino dos modelos de aprendizagem de máquina estatístico
'''
import os
import json
import joblib
from pandas import DataFrame
from numpyencoder import NumpyEncoder
from sklearn.model_selection import GridSearchCV, RepeatedStratifiedKFold

# TODO: Desenvolvimento de uma função que rode apenas um estimador mas que passe por todo o processo de otimização e de persistência com os devidos tratamentos de path, tipagem preparados para multithreading process.

class Training:
    def __init__(self):
        self.SEED = 42

    def training_model(self, x_train: DataFrame, y_train: DataFrame, estimator, grid: dict, scoring: str) -> None:
        '''
            Descrição:
            ----------
            Treina um estimador específico e otimiza seus hiperparâmetros utilizando Grid Search com validação cruzada por meio de Repeated Stratified KFold.

            Parâmetros:
            -----------
        '''

        grid_search = GridSearchCV(
            estimator=estimator,
            param_grid=grid,
            scoring=scoring,
            n_jobs=-1,
            cv=RepeatedStratifiedKFold(n_splits=2, n_repeats=2, random_state=self.SEED)
        )

        fitting = grid_search.fit(x_train, y_train)

        return fitting

    def save(self, x_test: DataFrame, model, output: str):
        try:
            proba = model.predict_proba(x_test)
        except:
            proba = []

        model_metadata= {
            'best_estimator_': model.best_estimator_,
            'best_params': model.best_params_,
            'best_score': model.best_score_,
            'y_pred': model.predict(x_test),
            'y_proba': proba
        }

        file_path = os.path.dirname(__file__)
        output_path = os.path.join(file_path, '../models', output)

        joblib.dump(model, output_path)

        output_metadata = os.path.join(
            file_path,
            '../data/processed',
            output.replace('.pkl', '_metadata.json')
        )

        with open(output_metadata, 'w') as jsonfile:
            json.dump(model_metadata, jsonfile, cls=NumpyEncoder)
