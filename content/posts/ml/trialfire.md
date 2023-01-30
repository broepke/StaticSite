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

Trialfire is a Marketing Attribution Platform.  While 

[Trialfire](https://trialfire.com)


## Motivation

In this article I will focus less on the the fundamentals of model building and more on the **overall thought process** in setting up the end-to-end process for moving this into production.  There will be references to best practices throughout as needed.

I am going to break this down into 3 steps:

* **Step 1**: Creating Queries for Our Model
* **Step 2**: Model Building with XGBoost
* **Step 3**: Inferencing on Fresh Data

In each of these steps, i'll explain the throught process and logic behind the steps.  

Let's go! 

## Step 1: Creating Queries for Our Model

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

Let's get our data.

### Keeping Your Dataset Balanced

I know from investigating this dataset that we have very [imbalanced data]({filename}../ml/imbalanced.md).  This is a common situtation where fewer people have purchased products than haven't.  I also know that this is a very large dataset.  I wanted to come up with an approach for training that would allow me to take a subset of the data but preserve the class balance.

I'll start by getting the counts of each class for the window of time that I intend to train my data on (which is essetially 6 months of data.  More on that shortly.)  I'm also utilizing a date-based constraint here where I'm fetching data where the user's `last_seen` data is older than 7 days but later than 6 months. In cases like this model, trying to predict purchase behavior, we don't want to go back too far with our data since multiple things could have changed such as ad campaigns, product offerings and more.  With Postgres, I can use the `INTERVAL` function to easily do this.

```python
true_counts = """
SELECT COUNT(*)
FROM person_""" + tf_api + """ P
WHERE (P.has_purchased is True) 
AND (P.last_seen < CURRENT_DATE - INTERVAL '7 days')
AND (P.last_seen > CURRENT_DATE - INTERVAL '6 months');
"""
```

I ended up with **46,5998** for the `true_counts` and **2,759,986** for the `false_counts`.  I simply used **25%** of these as limits store in a variable for the queries below.


### Building ML Ready Queries

Next our query.  There are actually three queries that are nearly identical.  The first two segment out data for both classes and the final data is people who haven't purchased that we want to predict their behavior on.  

1. `person_purchased` - People who have purchased in the past 6 months.  We will use this to train/test our model.
2. `person_not` - People who have not purchased in the past 6 months.  We will use this to train/test our model.
3. `person_test` - People who have not purchased but visited the site within the last 7 days.  We'll use this as our final validate set that we'll inference on.

### Feature Engineering

Before we explore the queries I want to cover how [Feature Engineering]({filename}../ml/featureeng.md)is **built right into the query** itself, as opposed to doing this during model building. 

Why is this critical and how did I arrive here? 

First of all.  I performed all of the [Exploratory Data Analysis]({filename}../ml/eda.md) and Feature Engineering inside my model building notebook.  I also performed [Feature Selection]({filename}../ml/featureselection.md), running the model multiple times until I settled on the final data I wanted.  

That won't be shown below, because after I performed all of these steps, I went back and built that **directly into the SQL query** statements.  What this allows me to do, is completely skip this step later when it comes to mode inference on new data! A hge time saver and improves the overal robustness of the model.  Let's take a look at a few steps.

1. `EXTRACT(EPOCH FROM (P.last_seen - P.first_seen))`: This select statement calculates the amount of seconds between the `last_seen` date and `first_seen` date.  This is super useful in figuring out how long a user has been visiting the site.  Also, utilizing EPOCH time instead of Date Diff is easier to work with since everything is normalized to a number of seconds.  When utilizing Date Diff, you can run into some that are in days, some are in milleseconds making it something you have to process again to normalize it.
2. `count(distinct)`, `sum()`, and `avg()` are all aggregate functions performed on the session table`: This is a great way to get a sense of how many times a user has visited the site, how many times they've clicked on a link, how many times they've input data, etc.  This is something you could reserve for Pandas, but it's much more efficient (and easier) to do right in your query.
3. `P.multi_device::int` and `P.has_purchased::int` this operation is casting a boolean value as an integer.  Working with integer values is needed for most ML models.  It's easier to get these into the correct format before moving forward.

You can extend this concept further with all of your feature engineering needs.  I highly reccomend doing it this way. 

### Etracting the Data for Specific Date Windows

Now let's run the actual queries that will extract our data.  As mentioned above, we don't want to go back too far in time with our data so we'll implement the same date window constraint we used for the counts above.  Two additional notes.  First I'm utilizing the function `RANDOM()` on the `ORDER BY` clause so that we return a random subset of data instead of something ordered.  Remember we're only pulling 25% of the total data availble.  Second, I've inserted the variable `str(lim_true)` into the `LIMIT` clause.  This is the variable we created earlier that holds the limit for the number of records we want to return.

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
AND (P.last_seen < CURRENT_DATE - INTERVAL '7 days')
AND (P.last_seen > CURRENT_DATE - INTERVAL '6 months')
GROUP BY P.person_id
ORDER BY random()
LIMIT """ + str(lim_true) + ';'
```

Then repeat the above for the `false_counts`.  Replacing `WHERE (P.has_purchased is True)` with `False` and `LIMIT """ + str(lim_true)` with `str(lim_false)`.

Now that we have our data representing our two classes, let's build a set of data that's **unseen** by the model.  In this case we'll take data where the user's last seen value is **greater than 7 days** ago.  We're not going to limit the number of records here like we did above.  We'll simply take all users who haven't purchased but that have visited in the last 7 days.

```python
person_test = """
SELECT ... (same as above)

WHERE (P.has_purchased is False) 
AND (P.last_seen > CURRENT_DATE - INTERVAL '7 days')
GROUP BY P.person_id;
"""
```

Now we can check the **shape** of each our our dataframes and persist them into `.pkl` files to make the data easier to work with and not have to run the queries again.

```python
print(df_purchased.shape)
print(df_not.shape)
print(df_test.shape)
```
```text
(116483, 23)
(689983, 23)
(265888, 23)
```

We have **116k** records for our purchased class, **690k** for our not purchased class, and **266k** for our validation set.  Check out the entire process and code for this portion on [GitHub](https://github.com/broepke/TrialFire/blob/main/01_tf_get_data.ipynb)


## Step 2: Model Building with XGBoost




1. [Model Selection]({filename}../ml/modelselection.md)
2. [Model Training and Evaluation]({filename}../ml/modeleval.md)




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
first_utm_medium               google_ads
first_utm_source                   search
multi_device                            0
session_count                           5
last_utm_medium                google_ads
last_utm_source                   display
source_category               Paid Search
source_category_2                 Branded
source_category_3                    None
seconds_since_first_vist      20218985.28
first_utm_content_distinct              1
first_utm_medium_distinct               1
first_utm_source_distinct               2
first_utm_term_distinct                 1
click_count_sum                        48
input_count_sum                         4
identify_count_sum                      2
view_count_sum                          1
page_count_sum                         72
source_category_distinct                4
session_duration_avg                  4.6
Name: 0, dtype: object
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
df_imp['SUMMED_TOTAL'] = df_imp['IMPORTANCE'].cumsum()
df_imp.head(10)
```
```text
                              FEATURE  IMPORTANCE  SUMMED_TOTAL
9             num__identify_count_sum    0.551607      0.551607
82        cat__first_utm_source_email    0.031941      0.583548
214  cat__source_category_Paid Search    0.028456      0.612005
196         cat__last_utm_source_sfmc    0.025089      0.637093
49        cat__first_utm_medium_email    0.025076      0.662169
182        cat__last_utm_source_email    0.014413      0.676583
11                num__page_count_sum    0.012657      0.689239
211        cat__source_category_Email    0.009739      0.698978
210      cat__source_category_Display    0.008529      0.707508
8                num__input_count_sum    0.007481      0.714989
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

           0      0.993     0.985     0.989    206899
           1      0.914     0.960     0.937     35041

    accuracy                          0.981    241940
   macro avg      0.954     0.972     0.963    241940
weighted avg      0.982     0.981     0.981    241940
```

![Pearson's Correlation Matrix]({static}../../images/posts/trialfire_cm.png)  


You can find all of the code for this portion of the process on [GitHub](https://github.com/broepke/TrialFire/blob/main/02_tf_first_purchase.ipynb)

## Step 3: Inferencing on Fresh Data


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

```text
PERSON_ID     PRED_DATE   CONVERT_PROB
051580b0      2023-01-29  1.0
985ad405      2023-01-29  0.9700000286102295
3f92a006      2023-01-29  0.8510000109672546
061cc82a      2023-01-29  0.7580000162124634
3ca4342a      2023-01-29  0.7509999871253967
122154d7      2023-01-29  0.75
```


```python
len(df_leads) / len(df)
```
```text
0.013900589721988205
```




You can find all of the code for this portion of the process on [GitHub](https://github.com/broepke/TrialFire/blob/main/03_tf_first_purchase_inference.ipynb)




https://docs.trialfire.com/#/sql_access?id=connecting

## Conclusion



As always, you can find the full code on [GitHub](https://github.com/broepke/TrialFire)


*If you liked what you read, [subscribe to my newsletter](https://campaign.dataknowsall.com/subscribe) and you will get my cheat sheet on Python, Machine Learning (ML), Natural Language Processing (NLP), SQL, and more. You will receive an email each time a new article is posted.*

## References

ecommerce Photo by <a href="https://unsplash.com/@cardmapr?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">CardMapr.nl</a> on <a href="https://unsplash.com/photos/pwxESDWRwDE?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>