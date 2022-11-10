from tabnanny import verbose
import numpy as np
import pandas as pd
import gc
from joblib import Parallel, delayed
import logging

logger = logging
logger.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


class Pandazip:
    """
    Class that gets a Pandas DataFrame and compresses its data to smallest
    feasible datatype per column.
    """

    def __init__(self, pandas_category=True, pandas_int=False, parallel=True, verbose=True):
        logger.info("Pandazip started")
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
        logger.info("Input size :{}".format(start_size))

        logger.info("Transforming available columns to numeric data type.")
        for col in data.columns:
            
            old_data = data[col].copy()
            old_dtype = old_data.dtype
            
            if pd.api.types.is_categorical_dtype(data[col]):
                continue
            
            data[col] = pd.to_numeric(data[col], errors='ignore')
            new_dtype = data[col].dtype
            
            if self.verbose and old_dtype!=new_dtype:
                logger.info('*'*100)
                logger.info(col)
                logger.info("Null Ratio: " + str(old_data.isna().sum() /len(old_data)))
                logger.info("------ OLD")
                logger.info(old_dtype)
                logger.info(old_data.head())
                
                logger.info("------ NEW")
                logger.info(new_dtype)
                logger.info(data[col].head())
            del old_data

        if self.parallel:
            logger.info("Parallel calculation...")
            data = Parallel(n_jobs=-1)(delayed(self._reduce)
                                                    (data[c]) for c in
                                                    data.columns)
            data = pd.concat(data, axis=1)
        else:
            data_li = []
            logger.info("Serial calculation...")
            for col in data.columns:
                
                #data[col] = self._reduce(data[col])
                temp_comp = self._reduce(data[col])
                if self.verbose and data[col].dtypes != data[col].dtypes:
                    logger.info(col)
                    logger.info(data[col].dtypes)
                    logger.info(temp_comp.dtypes)
                    
                data_li.append(temp_comp)
        data = pd.concat(data_li, axis=1)
        del data_li
        gc.collect()
        self.dtpes = data.dtypes

        final_size = round(data.memory_usage(deep=False).sum(), 2)
        logger.info("Output size: {}".format(final_size))
        logger.info("Compression rate: {}".format(round(((start_size -final_size) / final_size)*100, 2)))
        return data


    def transform(self, data):
        
        start_size = round(data.memory_usage(deep=False).sum(), 2)
        logger.info("Input size :{}".format(start_size))
        
        data_li = []
        for col, tp in self.dtpes.iteritems():
            data_li.append(data[col].astype(tp))
        
        data = pd.concat(data_li, axis=1)
        del data_li
        gc.collect()
        final_size = round(data.memory_usage(deep=False).sum(), 2)
        logger.info("Output size: {}".format(final_size))
        logger.info("Compression rate: {}".format(round(((start_size -final_size) / final_size)*100, 2)))
        
        return data



    def _reduce(self, s):
        s = pd.to_numeric(s, errors='ignore')
        coltype = s.dtype

        if np.issubdtype(coltype, np.integer):
            conv_key = 'int' if s.min() < 0 else 'uint'

        elif np.issubdtype(coltype, np.floating):
            if s.apply(float.is_integer).all():
                s = s.astype(int)
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
