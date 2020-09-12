
def main():
    from pandazip import Pandazip
    import pandas as pd
    import numpy as np
    from sklearn.datasets import load_breast_cancer
    print("Breast")
    cancer = load_breast_cancer()
    cancer = pd.DataFrame(np.c_[cancer['data'], cancer['target']],
                      columns=np.append(cancer['feature_names'], ['target']))
    score(cancer)
    cancer_low = Pandazip().zip(cancer, level="low")
    score(cancer_low)
    cancer_high = Pandazip().zip(cancer, level="high")
    score(cancer_high)
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
    data1 = pd.DataFrame(data=np.c_[iris['data'], iris['target']],
                         columns=iris['feature_names'] + ['target'])
    print("İris")
    score(data1)
    iris_low = Pandazip().zip(data1, level="low")
    score(iris_low)
    iris_high = Pandazip().zip(data1, level="high")
    score(iris_high)
    from sklearn import datasets
    import pandas as pd

    boston_data = datasets.load_boston()
    df_boston = pd.DataFrame(boston_data.data, columns=boston_data.feature_names)
    df_boston['target'] = pd.Series(boston_data.target)

    print("Boston")
    score(df_boston)
    df_boston_low = Pandazip().zip(df_boston, level="low")
    score(df_boston_low)
    df_boston_high = Pandazip().zip(df_boston, level="high")
    score(df_boston_high)


def score(data):
    from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
    try:
        rf = RandomForestClassifier()
        rf.fit(data.drop(columns = ["target"]), data["target"])
        print(rf.score(data.drop(columns = ["target"]), data["target"]))
    except:
        rf = RandomForestRegressor()
        rf.fit(data.drop(columns=["target"]), data["target"])
        print(rf.score(data.drop(columns=["target"]), data["target"]))

if __name__ == '__main__':
    main()

