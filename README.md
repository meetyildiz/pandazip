# pandazip
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)



<p align="center">
  <img src="https://github.com/meetyildiz/pandazip/blob/master/logo.png?raw=true" width="400" />
</p>

**Go minimal, go green, go pandazip.**


Cut memory footprint by forth in just 2 lines of code. 
Compress Pandas DataFrames without losing information or go smaller in expense of losing a bit of information.
Swift parallel execution makes pandazip very fast.


> "A 2018 blog post from OpenAI revealed that the amount of compute required for the largest AI training runs has increased by 300,000 times since 2012. And while that post didn’t calculate the carbon emissions of such training runs, others have done so. According to a paper by Emma Strubel and colleagues, an average American is responsible for about 36,000 tons of CO2 emissions per year; **training and developing one machine translation model** that uses a technique called neural architecture search was responsible for an estimated **626,000 tons of CO2**."

> "According to the American Council for an Energy-Efficient Economy it takes 5.12 kWh of electricity per gigabyte of transferred data. And according to the Department of Energy the average US power plant expends 600 grams of carbon dioxide for every kWh generated. That means that **transferring 1GB of data produces 3kg of CO2**."

plus storage and processing  = Huge impact on environment without even noticing.

**Take action now!**

## Install

pandazip can be installed from [PyPI](https://pypi.org/project/pandazip/):

<pre>
pip install pandazip
</pre>

## Compressing Pandas DataFrame using Pandazip

```python
from pandazip import Pandazip
zipper = Pandazip()
x_train = zipper.fit_transform(x_train)
x_test = zipper.transform(x_test)

```

