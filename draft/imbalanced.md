
Title: Working with Imbalanced Data
Date: 2021-11-07
Modified: 2021-11-07
Category: SQL
Tags: datascience, ml, machine learning, confusion matrix, scikit-learn, imblearn
Slug: imbalanced
Authors: Brian Roepke
Summary: Multiple techniques for dealing with imbalanced data from algorightm selection to synthetic data generation.
Header_Cover: images/botswana.jpg

## What is Imbalanced Data


## Different Methods for dealign with Imbalanced Data

1. Algorithme Selection
2. SMOTE


### SMOTE 

Synthetic Minority Oversampling Technique uses a nearest-neighbor approach for generating new minority class samples. The method is applied only to the training data and then tested on the original, untouched test partition. The method chosen here is first to oversample the minority class making it balanced, and then undersample it to reduce the size. This helps bring balance without bloating the dataset [4].


## Cross Validation

*stratified*!

## Evaluation Results

1. Accuracy
2. Precision
3. Recall
4. F1 Score




## References

1. [SMOTE: Synthetic Minority Over-sampling Technique](https://doi.org/10.1613/jair.953)
2. [SMOTE for Imbalanced Classification with Python](https://machinelearningmastery.com/smote-oversampling-for-imbalanced-classification/)
3. [Handling imbalanced datasets in machine learning](https://towardsdatascience.com/handling-imbalanced-datasets-in-machine-learning-7a0e84220f28)
