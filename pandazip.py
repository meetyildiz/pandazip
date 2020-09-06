import numpy as np
import pandas as pd
import time
import gc
from joblib import Parallel, delayed


def measure_time_mem(func):
    def wrapped_reduce(self, data, *args, **kwargs):
        # pre
        mem_usage_orig = data.memory_usage().sum() / self.memory_scale_factor
        start_time = time.time()
        # exec
        ret = func(self, data, *args, **kwargs)
        # post
        mem_usage_new = ret.memory_usage().sum() / self.memory_scale_factor
        end_time = time.time()
        """
        print(f'reduced data from {mem_usage_orig:.4f} MB '
              f'to {mem_usage_new:.4f} MB '
              f'in {(end_time - start_time):.2f} seconds')
        """
        gc.collect()
        return ret

    return wrapped_reduce


class Pandazip:
    """
    Class that takes a dict of increasingly big numpy datatypes to transform
    the data of a pandas dataframe into, in order to save memory usage.
    """
    memory_scale_factor = 1024 ** 2  # memory in MB

    def __init__(self, encode_cat=False, n_jobs=-1):
        """
        :param conv_table: dict with np.dtypes-strings as keys
        :param encode_cat: Whether the new pandas dtype "Categoricals"
                shall be used
        :param n_jobs: Parallelization rate
        """
        conv_table = None

        self.n_jobs = n_jobs

    def _type_candidates(self, k):
        for c in self.compress_lookup[k]:
            i = np.iinfo(c) if 'int' in k else np.finfo(c)
            yield c, i

    @measure_time_mem
    def zip(self, data, level="low", verbose=False):
        """Takes a dataframe and returns it with all data transformed to the
        smallest necessary types.

        :param data: pandas dataframe
        :param verbose: If True, outputs more information
        :return: pandas dataframe with reduced data types
        """
        if level == "low":
            self.compress_lookup = {'int': [np.int8, np.int16, np.int32, np.int64],
                                    'uint': [np.uint8, np.uint16, np.uint32, np.uint64],
                                    'float': [np.float16, np.float32, np.float64, ]}
            self.encode_cat = False

        elif level == "mid":
            self.compress_lookup = {'int': [np.int8, np.int16, np.int32],
                                    'uint': [np.uint8, np.uint16, np.uint32],
                                    'float': [np.float16, np.float32]}
            self.encode_cat = False

        elif level == "high":
            self.compress_lookup = {'int': [np.int8, np.int16],
                                    'uint': [np.uint8, np.uint16],
                                    'float': [np.float16]}
            self.encode_cat = True

        else:
            print("bad")

        start_size = round(data.memory_usage().sum() / 1024 ** 2, 2)
        print("Starting size is :{} MB".format(start_size))

        ret_list = Parallel(n_jobs=self.n_jobs)(delayed(self._reduce)
                                                (data[c], c, verbose) for c in
                                                data.columns)

        del data
        gc.collect()

        reduced_data = pd.concat(ret_list, axis=1)

        final_size = round(reduced_data.memory_usage().sum() / 1024 ** 2, 2)
        print("Finishing size is :{} MB".format(final_size))
        print("Compression rate is {}%".format(round(1 - final_size / start_size, 2)))
        return reduced_data

    def _reduce(self, s, colname, verbose):
        # skip NaNs
        if s.isnull().any():
            if verbose: print(f'{colname} has NaNs - Skip..')
            return s
        # detect kind of type
        coltype = s.dtype
        if np.issubdtype(coltype, np.integer):
            conv_key = 'int' if s.min() < 0 else 'uint'
        elif np.issubdtype(coltype, np.floating):
            conv_key = 'float'
        else:
            if isinstance(coltype, object) and self.encode_cat:
                # check for all-strings series
                if s.apply(lambda x: isinstance(x, str)).all():
                    if verbose: print(f'convert {colname} to categorical')
                    return s.astype('category')
            if verbose: print(f'{colname} is {coltype} - Skip..')
            return s
        # find right candidate
        for cand, cand_info in self._type_candidates(conv_key):
            if s.max() <= cand_info.max and s.min() >= cand_info.min:
                if verbose: print(f'convert {colname} to {cand}')
                return s.astype(cand)

        # reaching this code is bad. Probably there are inf, or other high numbs
        print(f"WARNING: {colname} doesn't fit the grid with \nmax: {s.max()} "
              f"and \nmin: {s.min()}")
        print('Dropping it..')