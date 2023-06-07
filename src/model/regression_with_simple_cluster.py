import pandas as pd
from sklearn.pipeline import Pipeline

from src.base.regression_model_base import RegressionModelBase
from src.repository.rent_data_loader import RentDataLoader
from src.base.column_name import RentDataCN, TimeDataCN, ClusterDataCN
from src.repository.weather_data_loader import WeatherDataLoader
from src.transform.transformer.cluster_column_extender import ClusterColumnExtender
from src.transform.transformer.custom_one_hot_encoder import CustomOneHotEncoder
from src.transform.transformer.data_concater import DataConcater
from src.transform.transformer.datetime_to_category import DatetimeToCategory
from src.transform.transformer.nighttime_dropper import NighttimeDropper
from src.transform.transformer.simple_cluster_aggregator import SimpleClusterAggregator
from src.transform.sampling.random_sampling import RandomSampling
from src.transform.transformer.location_column_extender import LocationColumnExtender
from src.transform.transformer.column_renamer import ColumnRenamer
from src.transform.transformer.string_to_datetime_converter import StringToDatetimeConverter
from src.transform.transformer.weather_column_extender import WeatherColumnExtender
from src.transform.transformer.weather_data_preprocessor import WeatherDataPreprocessor


class RegressionWithSimpleCluster(RegressionModelBase):
    def __init__(self):
        data_loader = RentDataLoader()
        weather_data_loader = WeatherDataLoader()

        weather_pipline = Pipeline([
            ('data_concatenate', DataConcater(data_category='weather')),
            ('renamer', ColumnRenamer()),
            ('str2datetime', StringToDatetimeConverter(data_category='weather')),
            ('preprocessor', WeatherDataPreprocessor())
        ])

        weather_data = weather_pipline.fit_transform(weather_data_loader.all_data)

        pipline = Pipeline([
            ('data_concatenate', DataConcater()),
            ('renamer', ColumnRenamer()),
            ('str2datatime', StringToDatetimeConverter(data_category='rent', per_hour=True)),
            ('location_extender', LocationColumnExtender(year="2021", only_rent_location=True)),
            ('cluster_extender', ClusterColumnExtender()),
            ('weather_extender', WeatherColumnExtender(preprocessed_data=weather_data)),
            ('datetime2category', DatetimeToCategory()),
            ('aggregate', SimpleClusterAggregator(is_categorical=True)),
            # ('dropper', NighttimeDropper()),
            ('one-hot_encode', CustomOneHotEncoder([TimeDataCN.MONTH, TimeDataCN.DAY, TimeDataCN.WEEKDAY]))
        ])

        self.__processed_data = pipline.fit_transform(data_loader.all_data)

        self.__processed_data = self.__processed_data[self.__processed_data[ClusterDataCN.CLUSTER] == 3]

        self.y = self.__processed_data[RentDataCN.RENT_COUNT]
        self.X = self.__processed_data.drop(columns=[RentDataCN.RENT_COUNT])

        super().__init__(self.X, self.y)