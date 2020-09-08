# pandazip






<p align="left">
  <img src="https://github.com/meetyildiz/pandazip/blob/master/logo.png?raw=true" width="300" />
</p>

**Pandazip**
Go minimal, go green, go pandazip

Cut memory footprint by half in just 2 lines of code. Compress Pandas DataFrame without/with losing information.


## Install

Shap can be installed from either [PyPI](https://pypi.org/project/pandazip):

<pre>
pip install pandazip
<i>or</i>
conda install -c conda-forge pandazip
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
