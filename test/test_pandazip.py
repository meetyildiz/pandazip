import pytest
import pandas as pd
import numpy as np
from pandazip.pandazip import Pandazip
from sklearn.datasets import load_breast_cancer, load_iris, fetch_california_housing

def test_memory_reduction_breast_cancer():
    cancer = load_breast_cancer()
    df = pd.DataFrame(np.c_[cancer['data'], cancer['target']],
                      columns=np.append(cancer['feature_names'], ['target']))

    initial_mem = df.memory_usage(deep=True).sum()
    zipper = Pandazip()
    compressed_df = zipper.fit_transform(df.copy())
    final_mem = compressed_df.memory_usage(deep=True).sum()

    assert final_mem < initial_mem
    pd.testing.assert_frame_equal(df.astype(compressed_df.dtypes), compressed_df)

def test_memory_reduction_iris():
    iris = load_iris()
    df = pd.DataFrame(data=np.c_[iris['data'], iris['target']],
                      columns=iris['feature_names'] + ['target'])

    initial_mem = df.memory_usage(deep=True).sum()
    zipper = Pandazip()
    compressed_df = zipper.fit_transform(df.copy())
    final_mem = compressed_df.memory_usage(deep=True).sum()

    assert final_mem < initial_mem
    pd.testing.assert_frame_equal(df.astype(compressed_df.dtypes), compressed_df)

def test_memory_reduction_california():
    housing = fetch_california_housing()
    df = pd.DataFrame(housing.data, columns=housing.feature_names)
    df['target'] = pd.Series(housing.target)

    initial_mem = df.memory_usage(deep=True).sum()
    zipper = Pandazip()
    compressed_df = zipper.fit_transform(df.copy())
    final_mem = compressed_df.memory_usage(deep=True).sum()

    assert final_mem < initial_mem
    pd.testing.assert_frame_equal(df.astype(compressed_df.dtypes), compressed_df)

@pytest.mark.parametrize("parallel", [True, False])
def test_fit_transform_consistency(parallel):
    # Create a dataframe with known values that can be downcasted
    data = {
        'small_int': [1, 2, 3], # should be int8
        'large_int': [10**10, 10**11, 10**12], # should be int64
        'float_col': [1.1, 2.2, 3.3], # should be float32/64
        'obj_col': ['a', 'b', 'a'] # should be category
    }
    df = pd.DataFrame(data)

    zipper = Pandazip(pandas_category=True, parallel=parallel)
    compressed = zipper.fit_transform(df.copy())

    assert compressed['small_int'].dtype == np.uint8
    assert compressed['large_int'].dtype == np.uint64
    assert compressed['obj_col'].dtype == 'category'
    pd.testing.assert_frame_equal(df.astype(compressed.dtypes), compressed)

def test_parallel_and_serial_results_match():
    df = pd.DataFrame({
        'small_int': [1, 2, 3],
        'negative_int': [-1, -2, -3],
        'large_int': [10**10, 10**11, 10**12],
        'float_col': [1.1, 2.2, 3.3],
        'obj_col': ['a', 'b', 'a'],
    })

    parallel_df = Pandazip(parallel=True).fit_transform(df.copy())
    serial_df = Pandazip(parallel=False).fit_transform(df.copy())

    pd.testing.assert_frame_equal(parallel_df, serial_df)

def test_transform_consistency():
    data_train = {'a': [1, 2], 'b': [100, 200]}
    data_test = {'a': [3, 4], 'b': [300, 400]}
    df_train = pd.DataFrame(data_train)
    df_test = pd.DataFrame(data_test)

    zipper = Pandazip()
    zipper.fit_transform(df_train)
    transformed_test = zipper.transform(df_test.copy())

    assert transformed_test['a'].dtype == np.uint8
    assert transformed_test['b'].dtype == np.uint8

def test_handle_incompatible_types_in_transform():
    # Train on numbers, transform something with strings in same column
    df_train = pd.DataFrame({'a': [1, 2]})
    df_test = pd.DataFrame({'a': ['not_a_number', 'still_not']})

    zipper = Pandazip()
    zipper.fit_transform(df_train)
    # This should not crash now thanks to our fix in transform()
    transformed = zipper.transform(df_test)

    assert str(transformed['a'].dtype) == 'Int64'
    assert pd.isna(transformed['a']).all() # because of errors='coerce'

@pytest.mark.parametrize("parallel", [True, False])
def test_string_dtype_converted_to_category(parallel):
    # Pandas may infer a dedicated string dtype instead of object
    df = pd.DataFrame({'obj_col': pd.Series(['a', 'b', 'a'], dtype='string')})

    zipper = Pandazip(pandas_category=True, parallel=parallel)
    compressed = zipper.fit_transform(df.copy())

    assert isinstance(compressed['obj_col'].dtype, pd.CategoricalDtype)
    assert compressed['obj_col'].tolist() == ['a', 'b', 'a']

def test_transform_preserves_category():
    df_train = pd.DataFrame({'c': pd.Series(['a', 'b', 'a'], dtype='category')})
    df_test = pd.DataFrame({'c': ['a', 'b']})

    zipper = Pandazip()
    zipper.fit_transform(df_train.copy())
    transformed = zipper.transform(df_test.copy())

    assert isinstance(transformed['c'].dtype, pd.CategoricalDtype)
    assert transformed['c'].tolist() == ['a', 'b']

def test_transform_preserves_nullable_int():
    df_train = pd.DataFrame({'x': [1.0, 2.0, 3.0]})
    df_test = pd.DataFrame({'x': [4.0, 5.0]})

    zipper = Pandazip(pandas_int=True)
    zipper.fit_transform(df_train.copy())
    transformed = zipper.transform(df_test.copy())

    assert str(transformed['x'].dtype) == 'Int64'
    assert transformed['x'].tolist() == [4, 5]


