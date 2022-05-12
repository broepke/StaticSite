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

1. Encoding categorical data
2. Calculate the difference between dates or times.
3. Aggregate data int a single row such as summing, counting, or calculating averages.
4. Converting text int a numerical values.
5. Merge data from different sources into a single set of observations.

According to [Wikipedia](https://en.wikipedia.org/wiki/Feature_engineering):

>Feature engineering or feature extraction is the process of using domain knowledge to extract features (characteristics, properties, attributes) from raw data. The motivation is to use these extra features to improve the quality of results from a machine learning process, compared with supplying only the raw data to the machine learning process.


BLAH BLAH

* Feature Engineering
* Feature Selection
* Feature Feature Importantce




## The Process of Feature Engineering

**RE-WRITE THIS**
(tasks before here…)
Select Data: Integrate data, de-normalize it into a dataset, collect it together.
Preprocess Data: Format it, clean it, sample it so you can work with it.
Transform Data: Feature Engineer happens here.
Model Data: Create models, evaluate them and tune them.
(tasks after here…)

* Brainstorm features: Really get into the problem, look at a lot of data, study feature engineering on other problems and see what you can steal.
* Devise features: Depends on your problem, but you may use automatic feature extraction, manual feature construction and mixtures of the two.
* Select features: Use different feature importance scorings and feature selection methods to prepare one or more “views” for your models to operate upon.
* Evaluate models: Estimate model accuracy on unseen data using the chosen features.

## Domain Knowledge

One of the critical parts of feature engineering is that you need to apply business and domain knowlege to your data in order to create the best features.  There isn't ever a single way or rule on how to create features, but many of the methods require you to know the context of why they might be relevant.

## Loading and Cleaning the Data

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
Data columns (total 7 columns):
 #   Column      Non-Null Count  Dtype 
---  ------      --------------  ----- 
 0   ACCOUNT_ID  1000 non-null   object
 1   OPP_ID      1000 non-null   object
 2   ORDER_DATE  1000 non-null   object
 3   PRODUCT     1000 non-null   object
 4   QUANTITY    1000 non-null   int64 
 5   START       998 non-null    object
 6   END         998 non-null    object
dtypes: int64(1), object(6)
memory usage: 54.8+ KB
```

```python
df_event.info()
```
```text
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 1048575 entries, 0 to 1048574
Data columns (total 7 columns):
 #   Column      Non-Null Count    Dtype 
---  ------      --------------    ----- 
 0   ACCOUNT_ID  1048575 non-null  object
 1   COMPANY_ID  1048575 non-null  object
 2   USER_ID     1048575 non-null  object
 3   PROJECT_ID  977461 non-null   object
 4   DATE        1048575 non-null  object
 5   TYPE        1048575 non-null  object
 6   COUNT       1048575 non-null  int64 
dtypes: int64(1), object(6)
memory usage: 56.0+ MB
```

```python
df_event.head()
```
```text
   ACCOUNT_ID COMPANY_ID USER_ID PROJECT_ID       DATE  \
0  account420       org1      u1         p1 2019-05-10   
1  account399       org2      u2         p2 2019-05-06   
2  account399       org2      u3         p3 2019-06-24   
3  account122       org3      u4         p4 2019-04-30   
4   account61       org4      u5         p5 2019-08-07   

                                                TYPE  COUNT  
0  099664351c56c479154c4b1e649a727e3ac099cc26747c...      3  
1  78478722fa50547376912d1bc1b21d5f5fb60188015342...      1  
2  9e5fd45ed38136db73e76b46ad11a0200b7a4cbaae9bc1...      2  
3  85c11686c1e1d3072f30b05ff74fd93b92c5d37a1b7ba3...      1  
4  31ea88da80c3371a7e70ac8a9299974290c47e83b46170...      1  
```

```python
df_opp.head()
```
```text
  ACCOUNT_ID OPP_ID ORDER_DATE  \
0   account1   opp1 2020-04-23   
1   account1   opp1 2020-04-23   
2   account2   opp2 2020-04-16   
3   account2   opp2 2020-04-16   
4   account3   opp3 2020-04-09   

                                             PRODUCT  QUANTITY
0  cd5ba48bb6ce3541492df6f2282ca555a65397c168dc59...         4
1  1a5a6aac31b1d9e08401bd147df106c600254b2df05a3f...         2
2  28746a25d12d36a1c0956436cfd6959f0db252e3020928...         1
3  1a5a6aac31b1d9e08401bd147df106c600254b2df05a3f...         8
4  1a5a6aac31b1d9e08401bd147df106c600254b2df05a3f...         3

  START         END  
0 2020-04-24    2021-04-23  
1 2020-04-24    2021-04-23  
2 2020-04-17    2021-04-16  
3 2020-04-17    2021-04-16  
4 2020-04-10    2021-04-09
```

```python
# Drop any null values from important variables
df_opp.dropna(subset=['START'], inplace=True)

# Fill any missing PROJECT_IDS with the COMPANY_ID
df_event['PROJECT_ID'].fillna(df_event['COMPANY_ID'], inplace=True)
```



## Understanding the Data Structure

Let's take a look at what this looks like visualized with an Entity Relationship Diagram.  I tend to this this is the best way to visualize tables of information because in a single image, we can see everything we need to know to understand how the data is strcutured from columns, data types, and the relationships between them.

In our first table, **OPPORTUNITIES**, we have a **composite key** that makes up the **primary key** cnsisting of **ACCOUNT_ID**, **OPPORTUNITY_ID**, **RENEWAL_DATE**, and **PRODUCT_CODE**.  The primary key allows us to uniquely identify an opportunity.  In the **EVENTS** table we have a **foreign key** relationship with **ACCOUNT_ID**.  For each account, we have **zero to many** potential events.

![ERD]({static}../../images/posts/featureeng_01.png)

## Encoding Categorical Data

One Hot Encoding

Ordinal Encoding


## Date Differences

First you need to make sure that any dates are actually in a date-time format

```python
# Convert dates to datetime type
df_event['DATE'] = pd.to_datetime(df_event['DATE'])
df_opp['ORDER_DATE'] = pd.to_datetime(df_opp['ORDER_DATE'])
df_opp['START'] = pd.to_datetime(df_opp['START'])
df_opp['END'] = pd.to_datetime(df_opp['END'])
```

Next, we can constuct new columns that represent the difference between the start and end dates.

```python
# Add a column for the number of days transpired since the last known event and the renewal date
df['DAYS_LAST_USED'] = (df['ORDER_DATE'] - df['DATE']).dt.days
```

## Aggregating Data Into Single Observations

```python
df_agg = df_event.groupby(['ACCOUNT_ID'], as_index=False).agg(
    {
        # how many unique projects are they using (more is better)
        'PROJECT_ID':"nunique", 
        
        # how many different unique orgs (more is better)
        'COMPANY_ID':"nunique", 
        
        # how many total unique users (more is better)
        'USER_ID':'nunique', 
        
        # are the using the software recently (more recent is better)
        'DATE':max, 
        
        # how many different features are they using (more is better)
        'TYPE':"nunique", 
        
        # what is their utilization (larger is better)
        'COUNT':sum 
    }
)

df_agg.head()
```
```text
   ACCOUNT_ID  PROJECT_ID  COMPANY_ID  USER_ID       DATE  TYPE  COUNT
0    account1           6           1        6 2019-09-23    21    216
1   account10         116           1       19 2019-10-23   309  87814
2  account100           9           1        5 2019-10-29   188   1582
3  account101           3           1        1 2019-09-18    31    158
4  account102          35           1        3 2019-10-30   214  14744
```




## Converting Text to Numerical Values


## An More!

Personal vs. Corporate Users



## Merging Datasets

```python
# Merge the datasets on Account ID
df = pd.merge(df_opp, df_agg, on="ACCOUNT_ID")
```



```python
# Reorder the columns by preference
df = df[['ACCOUNT_ID', 'OPP_ID', 'ORDER_DATE', 'PRODUCT', 'QUANTITY', 'START', 'END',
         'PROJECT_ID', 'DATE', 'DAYS_LAST_USED', 'TYPE', 'COUNT']]
df.head()
```
```text
  ACCOUNT_ID OPP_ID ORDER_DATE  \
0   account1   opp1 2020-04-23   
1   account1   opp1 2020-04-23   
2   account2   opp2 2020-04-16   
3   account2   opp2 2020-04-16   
4   account3   opp3 2020-04-09   

                                  PRODUCT    QUANTITY      START
0  cd5ba48bb6ce3541492df6f2282ca555a65...           4 2020-04-24
1  1a5a6aac31b1d9e08401bd147df106c6002...           2 2020-04-24
2  28746a25d12d36a1c0956436cfd6959f0db...           1 2020-04-17
3  1a5a6aac31b1d9e08401bd147df106c6002...           8 2020-04-17
4  1a5a6aac31b1d9e08401bd147df106c6002...           3 2020-04-10

         END  PROJECT_ID       DATE  DAYS_LAST_USED  TYPE  COUNT
0 2021-04-23           6 2019-09-23             213    21    216
1 2021-04-23           6 2019-09-23             213    21    216
2 2021-04-16          22 2019-10-16             183   185  19377
3 2021-04-16          22 2019-10-16             183   185  19377
4 2021-04-09          27 2019-10-08             184    64    556
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
