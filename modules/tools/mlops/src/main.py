import os

import pandas as pd

from imblearn.over_sampling import SMOTE

from catboost import CatBoostClassifier

from sklearn.svm import SVC # svm classifier
from sklearn.dummy import DummyClassifier  # dummy
from sklearn.tree import DecisionTreeClassifier  # tree baseds
from sklearn.linear_model import LogisticRegression  # linear models
from sklearn.neighbors import KNeighborsClassifier, RadiusNeighborsClassifier # neighbors based models
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier  # Ensemble estimators

def main():
    models = {
        'svc': SVC(),
        'dummy': DummyClassifier(),
        'knn': KNeighborsClassifier(),
        'adaboost': AdaBoostClassifier(),
        'catboost': CatBoostClassifier(),
        'rnn': RadiusNeighborsClassifier(),
        'decision_tree': DecisionTreeClassifier(),
        'random_forest': RandomForestClassifier(),
        'logistic_regression': LogisticRegression(),
        'gradient_boosting': GradientBoostingClassifier(),
    }

    static_grid = {
        'dummy': {
            'strategy': [
                'stratified',
                'most_frequent',
                'prior',
                'uniform',
                'constant'
            ]
        },
        'logistic_regression': {
            'solver': ['newton-cg', 'lbfgs', 'liblinear'],
            'penalty': ['l1', 'l2', 'elasticnet'],
            'C': [1, 5, 10, 50, 100, 200, 250, 300, 500, 1000, 5000]
        },
        'knn': {
            'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30],
            'metric': ['euclidean', 'manhattan', 'minkowski'],
            'weights': ['uniform', 'distance']
        },
        'rnn': {
            'radius': [0.1, 0.5, 1, 5, 10, 15, 20, 30, 50, 100, 500, 1000, 2000],
            'metric': ['euclidean', 'manhattan', 'minkowski'],
            'weights': ['uniform', 'distance']
        },
        'svc': {
            'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
            'C': [1, 2, 5, 10, 100, 200, 300, 400, 500]
        },
        'decision_tree': {
            'criterion': ['gini', 'entropy'],
            'splitter': ['random', 'best'],
            'max_depth': [35, 40, 45, 50, 55, 60, 65, 70, 350, 400, 450, 500, 1000],
            'min_samples_split': [0, 5, 10, 12, 14, 15],
            'min_samples_leaf': [0, 5, 10, 25, 50, 100, 200]
        },
        'random_forest': {
            'n_estimators': [10, 25, 50, 100, 200],
            'criterion': ['gini', 'entropy'],
            'max_depth': [5, 10, 20, 40, 50, 70, 80, 350, 400, 450, 500, 1000]
        },
        'gradient_boosting': {
            'loss': ['deviance', 'exponential'],
            'learning_rate': [0.1, 0.5, 1],
            'n_estimators': [10, 25, 50, 100, 200]
        },
        'adaboost': {
            'learning_rate': [0.1, 0.5, 1],
            'n_estimators': [10, 25, 50, 100, 200]
        },
        'catboost': {
            'n_estimators': [10, 25, 50, 100, 200],
            'learning_rate': [0.1, 0.5, 1],
            'max_depth': [5, 10, 20, 40, 50, 70, 80, 350, 400, 450, 500, 1000]
        }
    }

def run(x_train, x_test, y_train, name):

    scalers = [
        'default'
        'std',
        'minmax',
        'maxabs'
    ]

    for scaler in scalers:
        models_training(
            x_train=preprocessing.scaler(x_train, scaler),
            x_test=PrepareToTrain.scaler(x_test, scaler),
            y_train=y_train,
            scaler=f'{name}_{scaler}'
        )


if __name__ == '__main__':
    os.environ['PYTHONWARNINGS'] = 'ignore'

    df = pd.read_csv('../dados/output/processed_data.csv')

    SEED = 42

    x_train, x_test, y_train, y_test = PrepareToTrain.make_xy_split(df, 'sars_cov_2_exam_result')

    x_train.to_csv('../dados/output/x_train.csv', index=False)
    x_test.to_csv('../dados/output/x_test.csv', index=False)
    y_train.to_csv('../dados/output/y_train.csv', index=False)
    y_test.to_csv('../dados/output/y_test.csv', index=False)

    smote = SMOTE(random_state=SEED)
    x_train_resampled, y_train_resampled = smote.fit_resample(x_train, y_train)

    df_resampled = pd.concat([x_train_resampled, y_train_resampled], axis=1)
    df_resampled.to_csv('../dados/output/smote_resambled_train_data.csv', index=False)

    run(
    x_train=x_train,
    x_test=x_test,
    y_train=y_train,
    name='imb'
    )

    run(
        x_train=x_train_resampled,
        x_test=x_test,
        y_train=y_train_resampled,
        name='smote'
    )
