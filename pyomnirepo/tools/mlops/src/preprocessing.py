import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler

class Preprocessing:
    SEED = 42

    @staticmethod
    def filler(data, value):
        for col in data.select_dtypes(exclude='object'):
            data[col].fillna(value, inplace=True)

        return data

    @staticmethod
    def scaler(x, method):
        scaler = dict(
            std = StandardScaler(),
            minmax = MinMaxScaler(),
            maxabs = MaxAbsScaler()
        )

        x_scaled = pd.DataFrame(
            data=scaler[method].fit_transform(x),
            columns=x.columns
        )

        return x_scaled

    @classmethod
    def splitter(cls, df, target_feature):

        y = df[target_feature]
        x = df.drop(target_feature, axis=1)

        x_train, x_test, y_train, y_test = train_test_split(
            x,
            y,
            stratify=y,
            random_state=cls.SEED
        )

        x_train.reset_index(inplace=True)
        x_test.reset_index(inplace=True)

        return x_train, x_test, y_train, y_test
