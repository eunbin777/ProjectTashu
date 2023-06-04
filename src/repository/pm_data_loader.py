import os

import pandas as pd

from src.base.singleton_meta import SingletonMeta


class PMDataLoader(metaclass=SingletonMeta):
    def __init__(self, pm_data_information: dict = None):
        self.__FILE_PATH = os.path.dirname(os.path.abspath(__file__))
        self.__DATA_DIRECTORY = os.path.join(self.__FILE_PATH, "data")
        self.__PM_DATA = "PM"

        self.__pm_data_information = {
            "2022": (2022, None),
            "2021": (2021, None),
            "2020": (2020, None),
            "2019": (2019, None),
            "2018": (2018, None),
            "2017": (2017, None),
            "2016": (2016, None)
        } if pm_data_information is None else pm_data_information

        self.__all_pm_data = self.__load_all_data()

    def __load_data(self, year: int, encoding: str = None) -> pd.DataFrame:
        file_name = f"{self.__PM_DATA}_{year}.csv"
        csv_file = os.path.join(self.__DATA_DIRECTORY, file_name)
        data = pd.read_csv(csv_file, encoding=encoding)
        return data

    def __load_all_data(self) -> dict:
        result = dict()
        for key, value in self.__pm_data_information.items():
            result[key] = self.__load_data(*value)
        return result

    def get_specific_data(self, name: str) -> pd.DataFrame:
        if name not in self.__all_pm_data.keys():
            raise NameError(f"Name {name} is not in all_pm_data.")
        return self.all_data[name]

    @property
    def available_data_list(self) -> list:
        return list(self.__pm_data_information.keys())

    @property
    def all_data(self) -> dict:
        return self.__all_pm_data
