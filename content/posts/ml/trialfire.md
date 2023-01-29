Title: Predicting Which Users Will Convert to Paid With Trialfire and XGBoost
Date: 2023-01-31
Modified: 2023-01-31
Status: published
Tags: datascience, machine learning, marketing, analytics, python
Slug: trialfire
Authors: Brian Roepke
Summary: xxx
Description: xxx
Header_Cover: images/covers/marketing.jpg
Og_Image: images/covers/marketing.jpg
Twitter_Image: images/covers/marketing.jpg

# What is Trialfire?

Trialfire is a Marketing Attribution Platform.

[Trialfire](https://trialfire.com)


## Creating Queries for Our Model

One of the goals was to create queries that included all of the the selected features needed plus all feature engineering already performed.  By doing this, we can avoid a lot of clean up when we **inference** our model on new data.  I'll show the inferencing at the end of this article that will demonstrate how simple it is when you build clean data queries from the start.

Let's start by importing the required libraies. I'll be using the `psycopg2` library to connect to the database as well as `sqlalchemy` to create the connection string. 

```python
import pandas as pd
import psycopg2
import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus
```
I'll also utilize [Environment Variables]({filename}../other/envvar.md) for any of my sensitive information.  This prevents you from storing important information in your code but makes it as simple to retreive as one line of code.  Let's import all of them and save them as variables.

```python
tf_user = os.environ.get("TRIALFIRE_USER")
tf_pass = os.environ.get("TRIALFIRE_PASS")
tf_db = os.environ.get("TRIALFIRE_DB")
tf_host = os.environ.get("TRIALFIRE_HOST")
tf_api = os.environ.get("TRIALFIRE_API")
tf_port = 5432
```

Now we can build the connection string. I'm using the `quote_plus` function to ensure that any special characters are properly encoded.  This is especially important if you have a *username* or *password* with special characters.


```python
uri = f"postgresql+psycopg2://{quote_plus(tf_user)}:{quote_plus(tf_pass)}@{tf_host}:{tf_port}/{tf_db}"
alchemyEngine = create_engine(uri)
dbConnection = alchemyEngine.connect();
```

Let's start grabbing our data.

### Keeping Your Dataset Balanced

I know from investigating this dataset that we have very **imbalanced data**.  This is a common situtation.  In our case less people have purchased products than haven't.  I also know that this is a very large dataset.  I wanted to come up with an approach for training that would allow me to take a subset of the data but preserve the class balance.

For a guide on how to deal with Imbalanced Data, check out: [Don’t Get Caught in the Trap of Imbalanced Data When Building Your ML Model]({filename}../ml/imbalanced.md)

I'll start by getting the counts of each class for the window of time that I intend to train my data on (which is essetially 6 months of data.  More on that shortly.)

```python
# Us this to get the balance ratios to limit the number of rows
true_counts = """
SELECT COUNT(*)
FROM person_""" + tf_api + """ P
WHERE (P.has_purchased is True) 
AND (P.first_seen < CURRENT_DATE - INTERVAL '7 days')
AND (P.first_seen > CURRENT_DATE - INTERVAL '6 months');
"""
```

I ended up with **76,953** for the `true_counts` and **2,600,466** for the `false_counts`.  I simply used `10%` of these as limits for the queries below.


### Getting the Data

```python
person_purchased = """
SELECT
P.person_id, 
P.first_utm_medium,
P.first_utm_source,
P.multi_device::int, 
P.session_count,
P.last_utm_medium,
P.last_utm_source,
P.source_category,
P.source_category_2,
P.source_category_3, 
EXTRACT(EPOCH FROM (P.last_seen - P.first_seen)) as seconds_since_first_vist,
count(distinct S.first_utm_content) as first_utm_content_distinct,	
count(distinct S.first_utm_medium) as first_utm_medium_distinct,	
count(distinct S.first_utm_source) as first_utm_source_distinct,	
count(distinct S.first_utm_term) as first_utm_term_distinct,
sum(S.click_count) as click_count_sum,
sum(S.input_count) as input_count_sum,
sum(S.identify_count) as identify_count_sum,
sum(S.view_count) as view_count_sum,
sum(S.page_count) page_count_sum,
count(distinct S.source_category) as source_category_distinct,
avg(S.session_duration) as session_duration_avg,
P.has_purchased::int
FROM person_""" + tf_api + """ P
JOIN session_""" + tf_api + """ S 
ON S.person_id = P.person_id
WHERE (P.has_purchased is True) 
AND (P.first_seen < CURRENT_DATE - INTERVAL '7 days')
AND (P.first_seen > CURRENT_DATE - INTERVAL '6 months')
GROUP BY P.person_id
ORDER BY random()
LIMIT """ + str(lim_true) + ';'
```

Then repeat the above for the `false_counts`.  Replacing `WHERE (P.has_purchased is True)` with **False** and `LIMIT """ + str(lim_true)` with **lim_false**.

```python
person_test = """
SELECT

<< Trucated - Same as above with the following differences >>

WHERE (P.has_purchased is False) 
AND (P.last_seen > CURRENT_DATE - INTERVAL '7 days')
GROUP BY P.person_id;
"""
```


```python
print(df_purchased.shape)
print(df_not.shape)
print(df_test.shape)
```
```text
(7695, 23)
(260046, 23)
(251630, 23)
```

## Model Building


```python
import pandas as pd
import numpy as np
from collections import Counter
import warnings

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.compose import make_column_selector as selector
from sklearn.pipeline import Pipeline
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn import metrics 
from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import HalvingGridSearchCV

import xgboost as xgb

from joblib import dump, load

import matplotlib.pyplot as plt
import seaborn as sns
```


```python
df1 = pd.read_pickle('person_purchased.pkl')
df2 = pd.read_pickle('person_not.pkl')
df = pd.concat([df1, df2], axis=0)
df.shape
```
```text
(267741, 23)
```


```python
df["has_purchased"].value_counts()
```
```text
0    260046
1      7695
Name: has_purchased, dtype: int64
```

### Pearson Correlation


```python
corr = df.corr(numeric_only=True)

f, ax = plt.subplots(figsize=(12, 10))

sns.heatmap(corr, cmap="Blues", annot=True, square=False, ax=ax,  linewidth = 1)
plt.title('Pearson Correlation of Features')
plt.tight_layout()
plt.savefig('02_correlation_matrix.png', dpi=300);
```

![Pearson's Correlation Matrix]({static}../../images/posts/trialfire_corr.png)  

### Model Training

```python
df_y = df['has_purchased']
df_X = df.drop(columns=['has_purchased', 'person_id'])
```


```python
df_X.iloc[1]
```
```text
first_utm_medium                     sfmc
first_utm_source                    email
multi_device                            0
session_count                           5
last_utm_medium                google_ads
last_utm_source                    search
source_category               Direct Mail
source_category_2                    None
source_category_3                    None
seconds_since_first_vist      8579287.456
first_utm_content_distinct              1
first_utm_medium_distinct               2
first_utm_source_distinct               2
first_utm_term_distinct                 1
click_count_sum                        59
input_count_sum                         2
identify_count_sum                     11
view_count_sum                          0
page_count_sum                         55
source_category_distinct                4
session_duration_avg                  9.0
Name: 1, dtype: object
```


```python
# Split the data into 30% test and 70% training
X_train, X_test, y_train, y_test = train_test_split(df_X, df_y, test_size=0.3, random_state=0)
```


```python
# count examples in each class
counter = Counter(df_y)
# estimate scale_pos_weight value
estimate = counter[0] / counter[1]
print('Estimate: %.3f' % estimate)
```


```python
def create_pipe(clf):

    column_trans = ColumnTransformer(transformers=
        [('num', MinMaxScaler(), selector(dtype_include='number')),
        ('cat', OneHotEncoder(dtype='int', handle_unknown='ignore'), selector(dtype_include="object"))],
        remainder='passthrough', verbose_feature_names_out=True)

    pipeline = Pipeline([('prep',column_trans), ('clf', clf)])

    return pipeline
```


```python
clf = xgb.XGBClassifier(random_state=42, 
                        verbosity=0, 
                        objective='binary:logistic',
                        scale_pos_weight=estimate,
                        n_estimators=1000, 
                        max_depth=6, 
                        learning_rate=0.5)

pipeline = create_pipe(clf)
```




```python
pipeline.fit(X_train, y_train)
```


```python
feat_list = []
xgb_cols = get_feature_names(pipeline['prep'])
feat_imp = pipeline['clf'].feature_importances_

total_importance = 0
# Print the name and gini importance of each feature
for feature in zip(xgb_cols, feat_imp):
    feat_list.append(feature)
    total_importance += feature[1]
        
# create DataFrame using data
df_imp = pd.DataFrame(feat_list, columns =['FEATURE', 'IMPORTANCE']).sort_values(by='IMPORTANCE', ascending=False)
df_imp['CUMULATIVE_TOTAL'] = df_imp['IMPORTANCE'].cumsum()
df_imp.head(20)
```
```text
                                 FEATURE  IMPORTANCE  SUMMED_TOTAL
9                num__identify_count_sum    0.518808      0.518808
144           cat__source_category_Email    0.040660      0.559468
88           cat__last_utm_medium_criteo    0.037895      0.597363
161   cat__source_category_2_Retargeting    0.019294      0.616657
162     cat__source_category_2_Retention    0.017467      0.634124
61           cat__first_utm_source_email    0.014482      0.648606
160  cat__source_category_2_Reactivation    0.013840      0.662445
11                   num__page_count_sum    0.013448      0.675893
163           cat__source_category_2_SMS    0.012081      0.687974
152      cat__source_category_2_Facebook    0.011446      0.699420
```


https://johaupt.github.io/blog/columnTransformer_feature_names.html

```python
def print_confusion(pipeline):
    ''' take a supplied pipeline and run it against the train-test spit 
    and product scoring results.'''
    
    y_pred = pipeline.predict(X_test)

    print(metrics.classification_report(y_test, y_pred, digits=3))
        
    ConfusionMatrixDisplay.from_predictions(y_test, 
                                            y_pred, 
                                            cmap=plt.cm.Blues)

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig('02_confusion_matrix.png', dpi=300);
```


```python
print_confusion(pipeline)
```
```text
              precision    recall  f1-score   support

           0      0.997     0.995     0.996     77963
           1      0.839     0.902     0.869      2360

    accuracy                          0.992     80323
   macro avg      0.918     0.948     0.933     80323
weighted avg      0.992     0.992     0.992     80323
```

![Pearson's Correlation Matrix]({static}../../images/posts/trialfire_cm.png)  


## Inferencing on Fresh Data


```python
import pandas as pd
from joblib import load
```

```python
df = pd.read_pickle('person_test.pkl')
df.shape
```


```python
pipeline = load('02_tf_first_purchase.joblib')
```


```python
X = df.drop(columns=['has_purchased']).copy()
y = df['has_purchased'].copy()
X.shape
```


```python
# Predict the outcome variable based on the model
probs = pipeline.predict_proba(X)

# Get the Win probability for the `win` class
probs = probs[:,1]
probs = probs.round(3)

# Add the probability percentage to the DataFrame
X['last_prediction_date'] = pd.Timestamp.today().strftime('%Y-%m-%d')
X['convert_probability'] = probs.tolist()
```


```python
df_probs = X.sort_values('convert_probability', ascending=False)
df_leads = df_probs[df_probs['convert_probability'] >= 0.75]
df_leads[['person_id', 'last_prediction_date', 'convert_probability']].to_csv('03_tf_first_purchase_leads.csv', index=False)
```

```python
len(df_leads) / len(df)
```
```text
0.012685291896832651
```



As always, you can find the full code on [GitHub](https://github.com/broepke/TrialFire)

https://docs.trialfire.com/#/sql_access?id=connecting

## Conclusion



*If you liked what you read, [subscribe to my newsletter](https://campaign.dataknowsall.com/subscribe) and you will get my cheat sheet on Python, Machine Learning (ML), Natural Language Processing (NLP), SQL, and more. You will receive an email each time a new article is posted.*

## References

ecommerce Photo by <a href="https://unsplash.com/@cardmapr?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">CardMapr.nl</a> on <a href="https://unsplash.com/photos/pwxESDWRwDE?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>