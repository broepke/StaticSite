
Title: Working with Imbalanced Data
Date: 2021-11-25
Modified: 2021-11-25
Category: SQL
Tags: datascience, ml, machine learning, confusion matrix, scikit-learn, imblearn, imbalanced data
Slug: imbalanced
Authors: Brian Roepke
Summary: Multiple techniques for dealing with imbalanced data from algorightm selection to synthetic data generation.
Header_Cover: images/time.jpg
Og_Image: images/time.jpg
Twitter_Image: images/time.jpg

## What is Imbalanced Data

**Imbalanced data** is a case that is incredibly common in Machine Learning applications.  Imbalanced data occurs when you have a large number of observations in your data that represent one type of class and other classes that are much smaller. Examples of this might be fraudulent *credit card transactions* relative to legitimate purchases, or potentially *spam emails* relative to legitimate emails (It's also probable that legitimate emails are the minority these days).

## What is the Challenge? 

The challenge you will run into with imbalanced data is around how algorithms learn off of your data.  As you are building a train/test dataset, the number of observations in that represent the minority class will be much smaller than the majortiy.  The algorithm doesn't have enough data to truly model what the minority class will look like and ends up over-biasing to the majority class.  This can be espeically dangerous if you use a simply *Accuracy* metric to evaluate your model or when you are looking to have high precision or recall towards the minority class.  More on [evaluation metrics]({filename}/modeleval.md) later.

## Different Methods for dealign with Imbalanced Data

Fortunatley, with a little additional thought and setup in your training and testing phases, you can deal with imbalanced data, there are numerous ways to handle imbalanced data.  The following are some (not all) of the ways you can manage it:

1. Algorithme Selection
2. Generating synthetic data
3. Choosing the right performance metric

### Algorithme Selection

Let's start with the most simple way.  In this example I'll refer to Scikit-Lern's algoritm slection and how they handle imbalanced data.  Many of their algorithms support a `class_weight` parameter which can be set to `balanced`.  For example RandomForest, LogisticRegression, Perceptron, and SVM all support this parameter.  According to the [documentation](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html?highlight=class_weight): 


>**class_weight{“balanced”, “balanced_subsample”}, dict or list of dicts, default=None**  
>Weights associated with classes in the form `{class_label: weight}`. If not given, all classes are supposed to have weight one. For multi-output problems, a list of dicts can be provided in the same order as the columns of `y`.

>The “balanced” mode uses the values of `y` to automatically adjust weights inversely proportional to class frequencies in the input data as `n_samples / (n_classes * np.bincount(y))`

If during your model selection phase you find that one of these classifiers performs well, it's quite simple to use this feature of the agorithm to accomidate for 

### SMOTE

Synthetic Minority Oversampling Technique, or SMOTE, uses a nearest-neighbor approach for generating new minority class samples. The method is applied only to the training data and then tested on the original, untouched test partition. The method chosen here is first to oversample the minority class making it balanced, and then undersample it to reduce the size. This helps bring balance without bloating the dataset [^PAPER].

By synthetically generating minority class observations that are *similar* but not identitcal to other minority class observations, we can improve the performance of the model on the minority class.

The packgae [imblearn](https://imbalanced-learn.org/stable/index.html) contains the SMOTE algorithm and can very easily be integrated into SKLearn pipelines.  In addition to the SMOTE algorithm, there is also the ability to undersample the data bringing the data set back down to the original size.

**Note:** You must import the imblearn pipeline instead of the sklearn pipeline or it will not work.

```python
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

pipeline = Pipeline([('prep',column_trans),
                     ('over', SMOTE(random_state=42)),
                     ('under', RandomUnderSampler(random_state=42)),
                     ('clf', clf)])
```

## Cross Validation

*stratified*!

## Evaluation Results

Choosing the right evaluation metric is critical with imbalanced data.  If you're relying on Accuracy, then you're mostly likely not going to aceive the results you think you are.  Take a look at my other post on [Evaluating Models with a Confusion Matrix]({filename}/modeleval.md). 




## References

[^PAPER]: [SMOTE: Synthetic Minority Over-sampling Technique](https://doi.org/10.1613/jair.953)
[^IMBAL]: [Dealing with Imbalanced Data](https://towardsdatascience.com/methods-for-dealing-with-imbalanced-data-5b761be45a18)
[^SMOTE]: [SMOTE for Imbalanced Classification with Python](https://machinelearningmastery.com/smote-oversampling-for-imbalanced-classification/)