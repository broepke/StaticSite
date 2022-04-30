Title: Demystify Machine Learning Model Selection
Date: 2022-05-01
Modified: 2022-05-01
Status: draft
Tags: datascience, machine learning
Slug: modelselection
Authors: Brian Roepke
Summary: Leverage cross validation, performance metrics, and run time to determine the best model for your data.
Header_Cover: images/covers/choice.jpg
Og_Image: images/covers/choice.jpg
Twitter_Image: images/covers/choice.jpg


## What is Model Selection?


```python
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from timeit import timeit

import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.compose import ColumnTransformer

from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from sklearn.compose import make_column_selector as selector
from sklearn.pipeline import Pipeline
```


```python
df = pd.read_csv("bank.csv", delimiter=";")
df.shape
```
```text
(4521, 17)
```

```python
# check for nan/null
df.isnull().values.any()
# drop duplicates
len(df.drop_duplicates())
```

```python
# duration: last contact duration, in seconds (numeric). Important note: this attribute highly affects the output target (e.g., if duration=0 then y='no'). Yet, the duration is not known before a call is performed. Also, after the end of the call y is obviously known. Thus, this input should only be included for benchmark purposes and should be discarded if the intention is to have a realistic predictive model.
df.drop(columns='duration', inplace=True)
```

```python
X = df.iloc[:, :-1]
y = df.iloc[:,-1]
```

```python
enc = LabelEncoder()
enc.fit(y)
y = enc.transform(y)
```

```python
column_trans = ColumnTransformer(transformers=
        [('num', MinMaxScaler(), selector(dtype_exclude="object")),
        ('cat', OneHotEncoder(), selector(dtype_include="object"))],
        remainder='drop')
```

```python
# get a list of models to evaluate
def get_models():
    models = dict()
    
    # Decision Tree
    models['Logistic Regression'] = Pipeline([('prep', column_trans), ('model', LogisticRegression(random_state=42, max_iter=1000, class_weight='balanced'))])
    models['Decision Tree'] = Pipeline([('prep', column_trans), ('model', DecisionTreeClassifier(random_state=42, class_weight='balanced'))])
    models['Random Forest'] = Pipeline([('prep', column_trans), ('model', RandomForestClassifier(random_state=42, class_weight='balanced'))])
    models['Extra Trees'] = Pipeline([('prep', column_trans), ('model', ExtraTreesClassifier(random_state=42, class_weight='balanced'))])
    models['Gradient Boosting'] = Pipeline([('prep', column_trans), ('model', GradientBoostingClassifier(random_state=42))])
    models['Hist Gradient Boosting'] = Pipeline([('prep', column_trans), ('model', HistGradientBoostingClassifier(random_state=42))])
    models['AdaBoost'] = Pipeline([('prep', column_trans), ('model', AdaBoostClassifier(random_state=42))]) 
    models['SGD'] = Pipeline([('prep', column_trans), ('model', SGDClassifier(random_state=42, class_weight='balanced'))])
    models['SVC'] = Pipeline([('prep', column_trans), ('model', SVC(class_weight='balanced', random_state=42))])
    models['Nearest Neighbor'] = Pipeline([('prep', column_trans), ('model', KNeighborsClassifier(3))])
    models['Perceptron'] = Pipeline([('prep', column_trans), ('model', Perceptron(random_state=42))])
    
    return models
```

```python
# evaluate a give model using cross-validation
def evaluate_model(model, X, y):
    global scores
    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=1)
    scores = cross_val_score(model, X, y, scoring='roc_auc', cv=cv, n_jobs=-1)
    return scores
```

```python
# get the models to evaluate
models = get_models()

# evaluate the models and store results
results, names, time = list(), list(), list()
for name, model in models.items():
    %time scores = evaluate_model(model, X, y)
    results.append(scores)
    names.append(name)
    print('* %s Score = %.3f StdDev = (%.3f)' % (name, np.mean(scores), np.std(scores)), '\n')

# plot model performance for comparison
plt.figure(figsize=(10,8))
plt.boxplot(results, labels=names, showmeans=True)
plt.xticks(rotation=45)
```


```python
df_results = pd.DataFrame(list(zip(names, scores, time)),
               columns =['Name', 'Score', "Time"])
df_results.sort_values(by='Score', ascending=False, inplace=True)
df_results
```
```text
290 ms ± 0 ns per loop (mean ± std. dev. of 1 run, 1 loop each)
* Logistic Regression Score = 0.721 StdDev = (0.025) 

204 ms ± 0 ns per loop (mean ± std. dev. of 1 run, 1 loop each)
* Decision Tree Score = 0.573 StdDev = (0.021) 

1.61 s ± 0 ns per loop (mean ± std. dev. of 1 run, 1 loop each)
* Random Forest Score = 0.730 StdDev = (0.024) 

1.68 s ± 0 ns per loop (mean ± std. dev. of 1 run, 1 loop each)
* Extra Trees Score = 0.701 StdDev = (0.021) 

2.75 s ± 0 ns per loop (mean ± std. dev. of 1 run, 1 loop each)
* Gradient Boosting Score = 0.756 StdDev = (0.021) 

2.04 s ± 0 ns per loop (mean ± std. dev. of 1 run, 1 loop each)
* Hist Gradient Boosting Score = 0.728 StdDev = (0.021) 

886 ms ± 0 ns per loop (mean ± std. dev. of 1 run, 1 loop each)
* AdaBoost Score = 0.733 StdDev = (0.023) 

212 ms ± 0 ns per loop (mean ± std. dev. of 1 run, 1 loop each)
* SGD Score = 0.690 StdDev = (0.031) 

4.01 s ± 0 ns per loop (mean ± std. dev. of 1 run, 1 loop each)
* SVC Score = 0.715 StdDev = (0.027) 

660 ms ± 0 ns per loop (mean ± std. dev. of 1 run, 1 loop each)
* Nearest Neighbor Score = 0.608 StdDev = (0.022) 

127 ms ± 0 ns per loop (mean ± std. dev. of 1 run, 1 loop each)
* Perceptron Score = 0.639 StdDev = (0.043)                                               
```

![Default Settings]({static}../../images/posts/modelselection_01.png)


```python

```

```python

```


```python

```

## Conclusion



## References

Photo by Caleb Jones on Unsplash

search "choice"
