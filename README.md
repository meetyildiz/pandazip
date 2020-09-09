# pandazip
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/Naereen/StrapDown.js.svg)](https://GitHub.com/Naereen/StrapDown.js/issues/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)



<p align="center">
  <img src="https://github.com/meetyildiz/pandazip/blob/master/logo.png?raw=true" width="400" />
</p>

**Go minimal, go green, go pandazip.**


Cut memory footprint by half in just 2 lines of code. 
Compress Pandas DataFrame without/with losing information.
Swift parallel execution.


## Install

pandazip can be installed from [PyPI](https://pypi.org/project/pandazip/):

<pre>
pip install pandazip
</pre>

## Compressing Pandas DataFrame using Pandazip

```python
from pandazip import Pandazip
compressed_dataframe = Pandazip().zip(raw_dataframe)
```

## Lossless Compression

Compression level can be tuned with level parameter. Default is level="low", which is lossless. Every column is converted to the smallest datatype that can store column's data without losing information.

```python
compressed_dataframe = Pandazip().zip(raw_dataframe, level="low")
```

## Lossly Compression

When level parameter is set to "mid" or "high", Pazdazip limits numeric datatypes to 32 and 16 bits respectively. Also, string columns are converted to categoric datatype, if feasable.

```python
compressed_dataframe = Pandazip().zip(raw_dataframe, level="high")
```

## Results

Pandazip is tested on more than 100 Kaggle datasets and notebooks, feel free to share your results.

<p align="center">
  <img src="https://github.com/meetyildiz/pandazip/blob/master/pandazip results.png?raw=true" width="800" />
</p>

