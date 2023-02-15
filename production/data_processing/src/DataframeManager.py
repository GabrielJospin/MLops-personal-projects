import io
import json

import numpy as np
import pandas as pd
from scipy import stats as st
from Logger import Logger
from constants import *


class DataframeManager:
    def __init__(self) -> None:
        super().__init__()
        self.logger = Logger(__name__)

    def process_landed_files(self, landed_files_by_type, job_execution_id, file_manager):
        process_file = []
        for proc in PROCESS:
            for landed_file in landed_files_by_type[proc]:
                file_type = proc
                file_name = landed_file.key.split("/")[-1]
                js = self.get_meta(file_type, file_manager)
                file = file_manager.open(landed_file.key)
                self.logger.info(f'processing {landed_file.bucket_name}/{landed_file.key}')
                new_df = self.process(file, js)
                new_path = get_out_path(proc, job_execution_id, file_name)
                file_manager.save(new_df, new_path)
                file_manager.move_to_archive(file, proc, job_execution_id)
                file_manager.remove(landed_file.key)
                process_file.append(landed_file)
        return process_file

    @staticmethod
    def get_meta(file_type, file_manager):
        path = get_meta_path(file_type)
        file = file_manager.open(path)
        meta = json.loads(file.get()['Body'].read())
        return meta

    def process(self, file, js):
        df = pd.read_csv(io.BytesIO(file.get()['Body'].read()))
        num_of_columns = js["num_of_columns"]
        columns_config = js["columns"]
        method_of_normalization = js["method_of_normalization"]
        if len(df.columns) != num_of_columns:
            assert Exception("wrong number of columns")

        col_in, col_out = [], []
        for i in range(num_of_columns):
            col = columns_config[i]
            name = col["name"]
            variable = col["variable"]
            flow = col["flow"]
            df = self.clean(df, name, variable)
            if flow == "in":
                col_in.append(name)
            else:
                col_out.append(name)
        X = df.copy()
        X = self.norm(X, type_norm=method_of_normalization)
        for c in col_out:
            X.pop(c)
        y = df[col_out]

        new_df = pd.merge(left=X, right=y, left_index=True, right_index=True)
        print(np.array(new_df))
        return new_df

    def norm(self, df, type_norm="normalization"):
        if type_norm == "normalization":
            return self.normalization(df)
        if type_norm == "standardization":
            return self.standardization(df)

    def clean(self, df, name, variable):
        if variable == "categorical":
            return self.clean_categorical(df, name)
        if variable == "discrete":
            return self.clean_discrete(df, name)
        if variable == "continues":
            return self.clean_continues(df, name)
        if variable == "Binary":
            return self.clean_binary(df, name)
        return None

    @staticmethod
    def clean_categorical(dataset, column):
        series = dataset[column]
        types = series.unique()
        new = pd.DataFrame()

        for t in types:
            new[t] = np.zeros(len(dataset[column]))
            new[t][series == t] = 1

        new.pop(new.columns[-1])
        dataset.pop(column)
        dataset = pd.merge(dataset, new, left_index=True, right_index=True)
        return dataset

    def clean_discrete(self, df, name):
        return self.inputer(df, name, "median")

    def clean_continues(self, df, name):
        return self.inputer(df, name, "mean")

    @staticmethod
    def clean_binary(df, name):
        options = df[name].unique()
        for i, option in enumerate(options):
            df[name][df[name] == option] = i
        return df

    @staticmethod
    def inputer(dataset, column, mode="mean"):
        """

        :param dataset: dataset to be modified
        :param column: name or number of column to be modified
        :param mode: mean, median, mode or zero
        :return: dataset compleat
        """
        if mode not in ["mean", "median", "mode", "zero"]:
            assert Exception("mode invalid")
        values = dataset[column].values

        result = np.nan
        if mode == "mean":
            result = np.mean(values[~ np.isnan(values)])
        elif mode == 'median':
            result = np.median(values[~ np.isnan(values)])
        elif mode == 'mode':
            result = np.median(st.mode(values[~ np.isnan(values)]))
        elif mode == 'zero':
            result = 0

        values[np.isnan(values)] = result
        dataset[column] = values
        return dataset

    @staticmethod
    def normalization(dataset):
        """
        :param dataset: dataset
        :return: dataset normalized
        """
        for col in dataset.columns:
            max_v = np.max(dataset[col])
            min_v = np.min(dataset[col])
            series = (dataset[col] - min_v) / (max_v - min_v)
            dataset[col] = series
        return dataset

    @staticmethod
    def standardization(dataset):
        """
        :param dataset: dataset
        :return: dataset standardized
        """
        for col in dataset.columns:
            mean = np.mean(dataset[col])
            std = np.std(dataset[col])
            series = (dataset[col] - mean) / std
            dataset[col] = series
        return dataset
