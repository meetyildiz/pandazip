# pandazip






<p align="center">
  <img src="https://github.com/meetyildiz/pandazip/blob/master/logo-2.png?raw=true" width="300" />
</p>

---
<a href="https://travis-ci.org/slundberg/shap"><img src="https://travis-ci.org/slundberg/shap.svg?branch=master"></a>
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/slundberg/shap/master)

**Pandazip** 

Cut memory footprint by half in just three lines of code. Compress Pandas DataFrame without losing information.


## Install

Shap can be installed from either [PyPI](https://pypi.org/project/pandazip) or [conda-forge](https://anaconda.org/conda-forge/pandazip):

<pre>
pip install pandazip
<i>or</i>
conda install -c conda-forge pandazip
</pre>

## Compressing Pandas DataFrame using Pandazip

```python
from pandazip import Pandazip

# Initialize Pandazip
zipper = Pandazip()

# Compress Pandas DataFrame
compressed_dataframe = zipper.zip(raw_dataframe, level = "low")
```
