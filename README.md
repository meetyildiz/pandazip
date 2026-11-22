# pandazip

[![GitHub license](https://img.shields.io/github/license/meetyildiz/pandazip.svg)](https://github.com/meetyildiz/pandazip/blob/master/LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/meetyildiz/pandazip/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

<p align="center">
  <img src="https://github.com/meetyildiz/pandazip/blob/master/logo.png?raw=true" width="400" />
</p>

**Go minimal, go green, go pandazip.**

Cut memory footprint significantly in just 2 lines of code. Pandazip compresses
Pandas DataFrames by downcasting numeric columns to the smallest types that can
hold their values, and by turning low-cardinality string columns into
categoricals. Swift parallel execution makes pandazip very fast.

> "A 2018 blog post from OpenAI revealed that the amount of compute required for the largest AI training runs has increased by 300,000 times since 2012. And while that post didn’t calculate the carbon emissions of such training runs, others have done so. According to a paper by Emma Strubel and colleagues, an average American is responsible for about 36,000 tons of CO2 emissions per year; **training and developing one machine translation model** that uses a technique called neural architecture search was responsible for an estimated **626,000 tons of CO2**."

> "According to the American Council for an Energy-Efficient Economy it takes 5.12 kWh of electricity per gigabyte of transferred data. And according to the Department of Energy the average US power plant expends 600 grams of carbon dioxide for every kWh generated. That means that **transferring 1GB of data produces 3kg of CO2**."

plus storage and processing = huge impact on the environment without even noticing.

**Take action now!**

## Install

pandazip can be installed from [PyPI](https://pypi.org/project/pandazip/):

<pre>
pip install pandazip
</pre>

Requires `pandas` and `joblib`. Tested on Python 3.11–3.13 with pandas 3.x.

## Quick start

```python
from pandazip import Pandazip

zipper = Pandazip()
x_train = zipper.fit_transform(x_train)
x_test = zipper.transform(x_test)
```

`fit_transform` learns the compressed dtypes from the training frame and
returns the compressed frame. `transform` applies those learned dtypes to new
data.

## What it does

| Column kind | Result |
|---|---|
| Signed integers | Smallest signed type that fits (`int8` … `int64`) |
| Unsigned integers | Smallest unsigned type that fits (`uint8` … `uint64`) |
| Floats | `float16`, `float32` or `float64`, depending on range |
| Object / string | `category` when `pandas_category=True` |

Integer downcasts are lossless. Float downcasts preserve the value range but
may lose precision (for example, `1.1` does not survive a cast to `float16`).
With `pandas_int=True`, float columns whose values are all whole numbers are
converted to nullable `Int64` instead; columns with fractional values stay
floating-point.

## API

### `Pandazip(pandas_category=True, pandas_int=False, parallel=True, verbose=True)`

| Parameter | Default | Description |
|---|---|---|
| `pandas_category` | `True` | Convert object and string columns to `category`. When `False`, those columns are coerced to numeric and non-numeric values become `NaN`. |
| `pandas_int` | `False` | Convert float columns that contain only whole numbers to pandas' nullable `Int64`. Columns with fractional values stay floating-point. |
| `parallel` | `True` | Process columns in parallel with `joblib` (`n_jobs=-1`). Set to `False` for serial execution. |
| `verbose` | `True` | Print each column as it is processed. Summary lines are always printed. |

### `fit_transform(data)`

Learns the smallest suitable dtype for every column, stores them on the
instance, and returns the compressed DataFrame.

> **Note:** numeric columns of the input frame are converted in place. Pass
> `data.copy()` if you need the original frame to stay unchanged.

### `transform(data)`

Applies the dtypes learned by `fit_transform` to `data` and returns it.

- Columns that were not present during fitting are left untouched; fitted
  columns missing from `data` are skipped.
- Non-numeric values in numeric columns are coerced to `NaN`. If the learned
  dtype is a NumPy integer and `NaN`s are present, the column becomes nullable
  `Int64` instead.
- Category columns are cast to the learned categories. Values not seen during
  fitting become `NaN`.

## Development

```bash
pip install -r requirements-dev.txt
python -m pytest test/test_pandazip.py
```

The test suite runs on Python 3.11–3.13 via GitHub Actions.

## License

MIT — see [LICENSE](LICENSE).
