from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

from src.base.column_name import RentDataCN, WeatherDataCN


class DatetimeToCategory(BaseEstimator, TransformerMixin):
    """
    Datetime data to categorical data.
    """

    def __init__(self, data_category: str = 'rent'):
        if data_category == 'rent':
            self.__datetime_column = RentDataCN.RENT_DATE
        elif data_category == 'weather':
            self.__datetime_column = WeatherDataCN.DATE

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame, y=None):
        extended_X = self.categorical_datetime_extender(X)
        extended_X.drop(self.__datetime_column, axis=1, inplace=True)
        return X

    def categorical_datetime_extender(self, X: pd.DataFrame) -> pd.DataFrame:
        X['month'] = X[self.__datetime_column].dt.month
        X['day'] = X[self.__datetime_column].dt.day
        X['hour'] = X[self.__datetime_column].dt.hour
        X['weekday'] = X[self.__datetime_column].dt.weekday

        return X
