import numpy as np
import pandas as pd
import gc
from joblib import Parallel, delayed


class Pandazip:
    """
    Class that gets a Pandas DataFrame and compresses its data to smallest
    feasible datatype per column if level="low". If level is "mid" or "high",
    number data types are force to 32 and 16 bits respectively.
    """

    def __init__(self):
        print("Pandazip started", end="  /   ")
        self.pandas_category = False
        self.compress_lookup = {}
        self.n_jobs = -1

    def _type_candidates(self, k):
        for c in self.compress_lookup[k]:
            i = np.iinfo(c) if 'int' in k else np.finfo(c)
            yield c, i

    def zip(self, data, level="low"):
        """Takes a dataframe and returns it with all data transformed to the
        smallest necessary types.

        :param data: pandas dataframe
        :param level: string - "low", "mid", "high"
        :return: pandas dataframe with reduced data types
        """

        try:
            if level == "low":
                self.compress_lookup = {'int': [np.int8, np.int16, np.int32, np.int64],
                                        'uint': [np.uint8, np.uint16, np.uint32, np.uint64],
                                        'float': [np.float16, np.float32, np.float64, ]}
                self.pandas_category = False

            elif level == "mid":
                self.compress_lookup = {'int': [np.int8, np.int16, np.int32],
                                        'uint': [np.uint8, np.uint16, np.uint32],
                                        'float': [np.float16, np.float32]}
                self.pandas_category = True

            elif level == "high":
                self.compress_lookup = {'int': [np.int8, np.int16],
                                        'uint': [np.uint8, np.uint16],
                                        'float': [np.float16]}
                self.pandas_category = True

        except ValueError:
            print('level arg. must be either "low", "mid" or "high".')

        start_size = round(data.memory_usage().sum() / 1024 ** 2, 2)
        print("Input size :{} MB".format(start_size), end="  /   ")

        for col in data.columns:
            data[col] = pd.to_numeric(data[col], errors='ignore')

        ret_list = Parallel(n_jobs=self.n_jobs)(delayed(self._reduce)
                                                (data[c]) for c in
                                                data.columns)

        del data
        gc.collect()

        reduced_data = pd.concat(ret_list, axis=1)
        bool_cols = reduced_data.select_dtypes("bool").columns
        reduced_data[bool_cols] = reduced_data[bool_cols].astype(np.uint8)

        final_size = round(reduced_data.memory_usage().sum() / 1024 ** 2, 2)
        print("Output size: {} MB".format(final_size), end="  /   ")
        print("Compression rate: {}%".format(round((1 - final_size / start_size) * 100, 2)))
        return reduced_data

    def _reduce(self, s):

        # skip columns with null values
        if s.isnull().any():
            return s

        # detect data type
        coltype = s.dtype

        if np.issubdtype(coltype, np.integer):
            conv_key = 'int' if s.min() < 0 else 'uint'

        elif np.issubdtype(coltype, np.floating):
            conv_key = 'float'

        else:
            if isinstance(coltype, object) and self.pandas_category and s.apply(lambda x: isinstance(x, str)).all():
                return s.astype('category')

            return s

        # find right candidate
        for cand, cand_info in self._type_candidates(conv_key):
            if s.max() <= cand_info.max and s.min() >= cand_info.min:
                return s.astype(cand)

        return s.astype(cand)
