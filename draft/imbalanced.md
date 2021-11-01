
Title: Working with Imbalanced Data
Date: 2021-11-14
Modified: 2021-11-14
Category: SQL
Tags: datascience, ml, machine learning, confusion matrix, scikit-learn, imblearn, imbalanced data
Slug: imbalanced
Authors: Brian Roepke
Summary: Multiple techniques for dealing with imbalanced data from algorightm selection to synthetic data generation.
Header_Cover: images/time.jpg

## What is Imbalanced Data


## Different Methods for dealign with Imbalanced Data

1. Algorithme Selection
2. Generating synthetic data
3. Choosing the right performance metric


### Algorithme Selection

### SMOTE 

Synthetic Minority Oversampling Technique uses a nearest-neighbor approach for generating new minority class samples. The method is applied only to the training data and then tested on the original, untouched test partition. The method chosen here is first to oversample the minority class making it balanced, and then undersample it to reduce the size. This helps bring balance without bloating the dataset [4].


## Cross Validation

*stratified*!

## Evaluation Results

Choosing the right evaluation metric is critical with imbalanced data.  If you're relying on Accuracy, then you're mostly likely not going to aceive the results you think you are.  Take a look at my other post on [Evaluating Models with a Confusion Matrix](modeleval.html) 




## References

[^PAPER]: [SMOTE: Synthetic Minority Over-sampling Technique](https://doi.org/10.1613/jair.953)
[^IMBAL]: [Dealing with Imbalanced Data](https://towardsdatascience.com/methods-for-dealing-with-imbalanced-data-5b761be45a18)
[^SMOTE]: [SMOTE for Imbalanced Classification with Python](https://machinelearningmastery.com/smote-oversampling-for-imbalanced-classification/)