Title: Feature Engineering in Machine Learning
Date: 2022-05-14
Modified: 2022-05-14
Status: draft
Tags: datascience, machine learning
Slug: featureeng
Authors: Brian Roepke
Summary: Techniques for creating new features from data
Header_Cover: images/covers/engineering.jpg
Og_Image: images/covers/engineering.jpg
Twitter_Image: images/covers/engineering.jpg


## What is Feature Engineerring?

Feature Engineering in machine learning is the process of creating new feature from existing data. Often times with raw data, the information contained within may not be sufficent from a learning perspective.  Because of this, you may need to transform this data into new features, or columns that help you represent the data in a way that is more useful for learning.  A few examples of what might need to be done:

1. Aggregate data int a single row such as summing, counting, or calculating averages.
2. Calculate the difference between dates or times.
3. Converting text int a numerical value that represents business context.
4. Merge data from different sources into a single set of observations.

According to [Wikipedia](https://en.wikipedia.org/wiki/Feature_engineering):

>Feature engineering or feature extraction is the process of using domain knowledge to extract features (characteristics, properties, attributes) from raw data. The motivation is to use these extra features to improve the quality of results from a machine learning process, compared with supplying only the raw data to the machine learning process.


```python
import pandas as pd

df_opp = pd.read_csv('opps.csv')
df_event = pd.read_csv('events.csv')
```

```python
print(df_opp.shape)
print(df_event.shape)
```
```text
(1000, 8)
(1048575, 7)
```

```python
df_opp.info()
```
```text
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 1000 entries, 0 to 999
Data columns (total 8 columns):
 #   Column          Non-Null Count  Dtype 
---  ------          --------------  ----- 
 0   ACCOUNT_ID      1000 non-null   object
 1   OPPORTUNITY_ID  1000 non-null   object
 2   RENEWAL_DATE_C  1000 non-null   object
 3   PRODUCT_CODE    1000 non-null   object
 4   QUANTITY        1000 non-null   int64 
 5   START_DATE_C    998 non-null    object
 6   END_DATE_C      998 non-null    object
 7   IS_WON          580 non-null    object
dtypes: int64(1), object(7)
memory usage: 62.6+ KB
```

```python
df_event.info()
```
```text
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 1048575 entries, 0 to 1048574
Data columns (total 7 columns):
 #   Column           Non-Null Count    Dtype 
---  ------           --------------    ----- 
 0   ACCOUNT_ID       1048575 non-null  object
 1   ORGANIZATION_ID  1048575 non-null  object
 2   USER_ID          1048575 non-null  object
 3   PROJECT_ID       977461 non-null   object
 4   EVENT_TIME       1048575 non-null  object
 5   EVENT_TYPE       1048575 non-null  object
 6   EVENT_COUNT      1048575 non-null  int64 
dtypes: int64(1), object(6)
memory usage: 56.0+ MB
```

```python
# Convert dates to datetime type
df_event['EVENT_TIME'] = pd.to_datetime(df_event['EVENT_TIME'])
df_opp['RENEWAL_DATE_C'] = pd.to_datetime(df_opp['RENEWAL_DATE_C'])
df_opp['START_DATE_C'] = pd.to_datetime(df_opp['START_DATE_C'])
df_opp['END_DATE_C'] = pd.to_datetime(df_opp['END_DATE_C'])
```

## Aggregating Data Into Single Observations

```python
df_agg = df_event.groupby(['ACCOUNT_ID'], as_index=False).agg(
    {
        # how many unique projects are they using (more is better)
        'PROJECT_ID':"nunique", 
        # how many different unique orgs (more is better)
        'ORGANIZATION_ID':"nunique", 
        # how many total unique users (more is better)
        'USER_ID':'nunique', 
        # are the using the software recently (more recent is better)
        'EVENT_TIME':max, 
        # how many different features are they using (more is better)
        'EVENT_TYPE':"nunique", 
        # what is their utilization (larger is better)
        'EVENT_COUNT':sum 
    }
)

df_agg.head()
```
```text
   ACCOUNT_ID  PROJECT_ID  ORGANIZATION_ID  USER_ID EVENT_TIME  EVENT_TYPE  \
0    account1           6                1        6 2019-09-23          21   
1   account10         116                1       19 2019-10-23         309   
2  account100           9                1        5 2019-10-29         188   
3  account101           3                1        1 2019-09-18          31   
4  account102          35                1        3 2019-10-30         214   

   EVENT_COUNT  
0          216  
1        87814  
2         1582  
3          158  
4        14744  
```

## Date Differences

```python
# Add a column for the number of days transpired since the last known event and the renewal date
df['DAYS_LAST_USED'] = (df['RENEWAL_DATE_C'] - df['EVENT_TIME']).dt.days
```



## Merging Datasets

```python
# Merge the datasets on Account ID
df = pd.merge(df_opp, df_agg, on="ACCOUNT_ID")
```



```python
# Reorder the columns so our target is the last column
df = df[['ACCOUNT_ID', 'OPPORTUNITY_ID', 'RENEWAL_DATE_C', 'PRODUCT_CODE', 'QUANTITY', 'START_DATE_C', 'END_DATE_C',
         'PROJECT_ID', 'EVENT_TIME', 'DAYS_LAST_USED', 'EVENT_TYPE', 'EVENT_COUNT', 'IS_WON']]
df.head()
```
```text
  ACCOUNT_ID OPPORTUNITY_ID RENEWAL_DATE_C  \
0   account1           opp1     2020-04-23   
1   account1           opp1     2020-04-23   
2   account2           opp2     2020-04-16   
3   account2           opp2     2020-04-16   
4   account3           opp3     2020-04-09   

                                        PRODUCT_CODE  QUANTITY START_DATE_C  \
0  cd5ba48bb6ce3541492df6f2282ca555a65397c168dc59...         4   2020-04-24   
1  1a5a6aac31b1d9e08401bd147df106c600254b2df05a3f...         2   2020-04-24   
2  28746a25d12d36a1c0956436cfd6959f0db252e3020928...         1   2020-04-17   
3  1a5a6aac31b1d9e08401bd147df106c600254b2df05a3f...         8   2020-04-17   
4  1a5a6aac31b1d9e08401bd147df106c600254b2df05a3f...         3   2020-04-10   

  END_DATE_C  PROJECT_ID EVENT_TIME  DAYS_LAST_USED  EVENT_TYPE  EVENT_COUNT  \
0 2021-04-23           6 2019-09-23             213          21          216   
1 2021-04-23           6 2019-09-23             213          21          216   
2 2021-04-16          22 2019-10-16             183         185        19377   
3 2021-04-16          22 2019-10-16             183         185        19377   
4 2021-04-09          27 2019-10-08             184          64          556   

  IS_WON  
0    NaN  
1    NaN  
2   True  
3   True  
4   True  
```

```python
df.shape
```
```text
(949, 13)
```




## Conclusion



## References

Photo by Vishnu Mohanan on Unsplash
https://unsplash.com/@vishnumaiea?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText
