# pandazip






<p align="center">
  <img src="https://github.com/meetyildiz/pandazip/blob/master/logo-2.png?raw=true" width="300" />
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
compressed_dataframe = Pandazip().zip(raw_dataframe, level = "low")
```
