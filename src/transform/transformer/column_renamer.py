from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

from src.base.column_name import RentDataCN, WeatherDataCN, PmDataCN


class ColumnRenamer(BaseEstimator, TransformerMixin):
    """
    Renaming column to english.
    """

    def __init__(self):
        pass

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame, y=None):
        return self.renaming(X)

    # noinspection PyMethodMayBeStatic
    def renaming(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.rename(columns={
            '대여스테이션': RentDataCN.RENT_STATION,
            '대여일시': RentDataCN.RENT_DATE,
            '반납스테이션': RentDataCN.RETURN_STATION,
            '반납일시': RentDataCN.RETURN_DATE,
            '이동거리': RentDataCN.DISTANCE,
            '회원구분': RentDataCN.USER_CATEGORY,
            '지점': WeatherDataCN.ID,
            '지점명': WeatherDataCN.NAME,
            '일시': WeatherDataCN.DATE,
            '기온(°C)': WeatherDataCN.TEMPERATURE,
            '강수량(mm)': WeatherDataCN.PRECIPITATION,
            '풍속(m/s)': WeatherDataCN.WIND_SPEED,
            '습도(%)': WeatherDataCN.HUMIDITY,
            '일조(hr)': WeatherDataCN.SUNSHINE_DURATION,
            '현상번호(국내식)': WeatherDataCN.WEATHER_NUMBER,
            '지면온도(°C)': WeatherDataCN.GROUND_TEMPERATURE,
            '날짜':PmDataCN.DATE,
            '대덕구': PmDataCN.DAEDEOKGU,
            '동구': PmDataCN.DONGGU,
            '서구': PmDataCN.SEOGU,
            '유성구': PmDataCN.YUSEONGGU,
            '중구': PmDataCN.JUNGGU
        })
