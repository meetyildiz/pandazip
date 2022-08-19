from tabnanny import verbose
import numpy as np
import pandas as pd
import gc
from joblib import Parallel, delayed


class Pandazip:
    """
    Class that gets a Pandas DataFrame and compresses its data to smallest
    feasible datatype per column.
    """

    def __init__(self, pandas_category=True, pandas_int=False, parallel=True, verbose=True):
        print("Pandazip started")
        self.pandas_category = pandas_category
        self.pandas_int = pandas_int
        self.parallel = parallel
        self.verbose = verbose

    def fit_transform(self, data):

        self.compress_lookup  = {'pint': ["Int64"],
                                'int': [np.int8, np.int16, np.int32, np.int64],
                                'uint': [np.uint8, np.uint16, np.uint32, np.uint64],
                                'float': [np.float16, np.float32, np.float64, ]}

        start_size = round(data.memory_usage(deep=False).sum(), 2)
        print("Input size :{}".format(start_size))

        print("Transforming available columns to numeric data type.")
        for col in data.columns:
            if verbose:
                print(col)
            data[col] = pd.to_numeric(data[col], errors='ignore')


        if self.parallel:
            print("Parallel calculation...")
            data = Parallel(n_jobs=-1)(delayed(self._reduce)
                                                    (data[c]) for c in
                                                    data.columns)
            data = pd.concat(data, axis=1)
        else:
            print("Serial calculation...")
            for col in data.columns:
                if verbose:
                    print(col)
                data[col] = self._reduce(data[col])
        
        gc.collect()
        self.dtpes = data.dtypes

        final_size = round(data.memory_usage(deep=False).sum(), 2)
        print("Output size: {}".format(final_size))
        print("Compression rate: {}".format(round((start_size / final_size)*100, 2)))
        return data


    def transform(self, data):

        for col, tp in self.dtpes.iteritems():
            data[col] = data[col].astype(tp)
        
        return data



    def _reduce(self, s):
        s = pd.to_numeric(s, errors='ignore')
        coltype = s.dtype

        if np.issubdtype(coltype, np.integer):
            conv_key = 'int' if s.min() < 0 else 'uint'

        elif np.issubdtype(coltype, np.floating):
            if self.pandas_int:
                return s.astype('Int64')
            else:
                conv_key = 'float'


        else:
            if isinstance(coltype, object) and self.pandas_category:
                return s.astype('category')

            return s

        # find right candidate
        for cand, cand_info in self._type_candidates(conv_key):
            if s.max() <= cand_info.max and s.min() >= cand_info.min:
                return s.astype(cand)

        return s.astype(cand)

    def _type_candidates(self, k):
        for c in self.compress_lookup[k]:
            i = np.iinfo(c) if 'int' in k else np.finfo(c)
            yield c, i
