Title: Eploratory Data Analysis
Date: 2021-12-04
Modified: 2021-12-04
Status: draft
Category: EDA
Tags: datascience, machine learning, eda, data
Slug: eda
Authors: Brian Roepke
Summary: My approach to EDA; One of the most critical steps in your project.
Header_Cover: images/road.jpg
Og_Image: images/road.jpg
Twitter_Image: images/road.jpg

## What is EDA?

EDA, or Exploratory Data Analysis, is the process of examining and understanding the structure of a dataset.  It's a critical part of any machine learning project and it is the tool in your toolbox that allows you to approach data you've never need before, and get comfortable with all sorts of charicteristics.

I find that a lot of people jump right into their data without first properly performing EDA.  Especially after they've done a few projects and think they know what they're doing.  To me, this is a critical first step that uncovers so manny hidden gems in the data it's indespensible.

## My Appraoch to EDA

This is the generalized process I use to perform EDA.  It can very from dataset to dataset, depending on the type of data, the complexity, and the messiness.  However, these steps are generally the same for all datasets.

1. Basic Exploration
2. Check for Null & Duplicate Values
3. Dealing with Outliers
4. Visualize the Data

## Basic Exploration

Start by importing the needed packages.  These are my goto defaults for all fresh explorations.  I tend to find `seaborn` is a really conventient wrapper on top of `matplotlib` that helps you build visualations faster.

```python
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
```

### See the Size, Columns, and Sample Rows

After I import data there are a few functions from `pandas` that I run before anything else.  Let's go throught them.

```python
df.shape
```
```text
(4521, 17)
```

We can see from the output there are `4,521` observations with `17` columns.

```python
df.info()
```
```text
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 4521 entries, 0 to 4520
Data columns (total 17 columns):
 #   Column     Non-Null Count  Dtype 
---  ------     --------------  ----- 
 0   age        4521 non-null   int64 
 1   job        4521 non-null   object
 2   marital    4521 non-null   object
 3   education  4521 non-null   object
 4   default    4521 non-null   object
 5   balance    4521 non-null   int64 
 6   housing    4521 non-null   object
 7   loan       4521 non-null   object
 8   contact    4521 non-null   object
 9   day        4521 non-null   int64 
 10  month      4521 non-null   object
 11  duration   4521 non-null   int64 
 12  campaign   4521 non-null   int64 
 13  pdays      4521 non-null   int64 
 14  previous   4521 non-null   int64 
 15  poutcome   4521 non-null   object
 16  y          4521 non-null   object
dtypes: int64(7), object(10)
memory usage: 600.6+ KB
```

The way that `pandas` imports data is to give the best guess at datatypes.  You can change them later if they didn't import properly.  In my case above, it looks like most of the data types are `integers` and `objects` or strings.

Next, simply display the first and last few rows of data.

```python
df.head()
```
and
```python
df.tail()
```

### See a Statistical Summary

There is a super powerful command that in a single function, `df.describe()` can give you a birds-eye view of your data.  It will show counts, mean, standard deviation, min, max, and more.  With this data you can get a pretty good sense of what you're up against, however, visualizing this later will add to your analysis.

```python
# Without an parameters passed into the describ function, it will return numerical only.
df.describe().round(2)
```
```text
           age   balance      day  duration  campaign    pdays  previous
count  4521.00   4521.00  4521.00   4521.00   4521.00  4521.00   4521.00
mean     41.17   1422.66    15.92    263.96      2.79    39.77      0.54
std      10.58   3009.64     8.25    259.86      3.11   100.12      1.69
min      19.00  -3313.00     1.00      4.00      1.00    -1.00      0.00
25%      33.00     69.00     9.00    104.00      1.00    -1.00      0.00
50%      39.00    444.00    16.00    185.00      2.00    -1.00      0.00
75%      49.00   1480.00    21.00    329.00      3.00    -1.00      0.00
max      87.00  71188.00    31.00   3025.00     50.00   871.00     25.00
```

### Inspect Categorical Values

The following function is a really handy one when dealing with categorical data.  It first selects just the columns of type `object`, in our case all of the text fields are truly categorical. Then it loops over each of those columns and prints the `value_counts` of each.

```python
# get categorical data
cat_data = df.select_dtypes(include=['object'])
# show counts values of each categorical variable
for colname in cat_data.columns:
    print (colname)
    print (cat_data[colname].value_counts(), '\n')
```
here is what an example output looks like for a single column.  Notice how great that summarizes categorical data.

```text
marital
married     2797
single      1196
divorced     528
Name: marital, dtype: int64 
```

## Check for Null & Duplicate Values

### Null Values

The next step I perform is checking for null values.  Null values are often not allowed in a Machine learning model, so it's important to deal with them.  It will take a bit of exploration and interpretation to know *how* you want to deal with them.  It can range from simply dropping them when there are a very small amount, filling them with a default value such as `0` or filling them based on adjacent values.  This method is common with time series data where you might fill a missing value with the mean of the prior and following values.  Pandas has extensive support with there `fillna()` function that you can read about [here](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.fillna.html).

For this example I'll explore if there are any, and drop them from the dataset.

```python
# check for nan/null
df.isnull().values.any()
# count of nulls per column
df.isnull().sum()
```
and to drop them

```python
# Drop NULL values
df.dropna(inplace=True)
```

### Duplicate Values

Next in order is to look for duplicates.  Duplicates are similar to null values in the fact that they need to be interpreated as actual clean, useful data, or erroneous data.  Duplicates can also be a problem in Machine Learning because they could cause your model to overbias to observations that aren't part of the true dataset.  You can utilize the below code to either check for duplicates or to drop them as is implemented here:

```python
len_before = df.shape[0]
df.drop_duplicates(inplace=True)
len_after = df.shape[0]

print(f"Before = {len_before}")
print(f"After = {len_after}")
print("")
print(f"Total Removed = {len_before - len_after}")
```
```text
Before = 4521
After = 4521

Total Removed = 0
```

In this case, there were no duplicate rows or null values, but it's very important to check and handle them appropriately for your usecase.

## Dealing with Outliers


## Visualize the Data

I like to break my visualizations into two different parts.  Explicitly first utilizing only univariate plots, or plots such as histograms and boxplots on *single* variables.  Then I tend to layer in bivariate (or multi-variate) plots across different variables.  This process helps me to break down the analysis into the layers of understanding of the data.

### Univariate Plots

A univariate plot is exactly as it sounds-a plot agasint a single variable.  Let's start by looking at box plots of all the numeric variables in the dataset.

```python
# using seaborn library, plot each individually
fig, axes = plt.subplots(3, 2, figsize=(14,14))

ax = sns.boxplot(x="y", y="age", data=df, ax=axes[0, 0])
ax = sns.boxplot(x="y", y="balance", data=df, ax=axes[0, 1])
ax = sns.boxplot(x="y", y="duration", data=df, ax=axes[1, 0])
ax = sns.boxplot(x="y", y="campaign", data=df, ax=axes[1, 1])
ax = sns.boxplot(x="y", y="pdays", data=df, ax=axes[2, 0])
ax = sns.boxplot(x="y", y="previous", data=df, ax=axes[2, 1])
```



### Bivariate Plots


## Conclusion

EDA is a very powerful technique that you should get comfortable with and you should do every time you start workign on a new dataset.  There are plenty of other tecniques out there that you can add to these basics.  Go out there, explore and get to know your data before you jump into machine learning.

All the code above is avaiable in [Github](https://github.com/broepke/EDA).

## References

Photo by <a href="https://unsplash.com/@amanda_sandlin?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Amanda Sandlin</a> on <a href="https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
  

[^EDA]: [How And Why Exploratory Data Analysis — EDA used in Python Data Analysis](https://soorajsknair.medium.com/how-and-why-exploratory-data-analysis-eda-used-in-python-data-analysis-db451394eb7f)
[^OUTS]: [How to Remove Outliers for Machine Learning](https://machinelearningmastery.com/how-to-use-statistics-to-identify-outliers-in-data/)