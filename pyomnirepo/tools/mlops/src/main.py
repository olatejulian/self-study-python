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
    {
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
