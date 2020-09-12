
import pandas as pd
import numpy as np
from sklearn.datasets import load_breast_cancer
from pandazip.pandazip import Pandazip


cancer = load_breast_cancer()
df = pd.DataFrame(np.c_[cancer['data'], cancer['target']],
                  columns = np.append(cancer['feature_names'], ['target']))

print(Pandazip().zip(df, level="low"))
"""
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris

# save load_iris() sklearn dataset to iris
# if you'd like to check dataset type use: type(load_iris())
# if you'd like to view list of attributes use: dir(load_iris())
iris = load_iris()

# np.c_ is the numpy concatenate function
# which is used to concat iris['data'] and iris['target'] arrays
# for pandas column argument: concat iris['feature_names'] list
# and string list (in this case one string); you can make this anything you'd like..
# the original dataset would probably call this ['Species']
data1 = pd.DataFrame(data= np.c_[iris['data'], iris['target']],
                     columns= iris['feature_names'] + ['target'])

print(Pandazip().zip(data1, level="low"))


print(Pandazip().zip(data1, level="high"))



from sklearn import datasets
import pandas as pd

boston_data = datasets.load_boston()
df_boston = pd.DataFrame(boston_data.data,columns=boston_data.feature_names)
df_boston['target'] = pd.Series(boston_data.target)

print(Pandazip().zip(df_boston, level="low"))


print(Pandazip().zip(df_boston, level="high"))
"""