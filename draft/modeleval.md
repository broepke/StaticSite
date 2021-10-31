Title: Evaluating Models with a Confusion Matrix
Date: 2021-11-24
Modified: 2021-11-24
Category: SQL
Tags: datascience, ml, machine learning, confusion matrix
Slug: modeleval
Authors: Brian Roepke
Summary: How to evaluate models using a confusion matrix and when to use different metrics.
Header_Cover: images/confused.jpg

## Model Evaluation for Binary Classification

Understanding how to evaluate models is a critical part of any Machine Learning (ML) project.  Many times when we're starting with ML or when having conversations with people that aren't as well versed in ML, the term **Accuracy** is thrown out as a generalization of the model's performance.  The problem with generally talking about the **Accuracy** is that it specifically refers to the overall performance of the model's ability to predict both the positive or the negative classes in the dataset.

While **Accuracy** is acceptable for model performance when your dataset is perfectly balanced (equal positive and negative classes), the reality is that this is rarely the case.  There are methods to deal with imbalanced data, which I'll talk about later, but for now, let's understand how to interpret the results of a model's performance properly.

## Interpreting a Confusion Matrix

After a model is trained and tested on data (Scikit-Learn has a great write-up of this process[^CROSS]), you can use a Confusion Matrix to give a view of how many observations the model misclassified.  The trick to this is not just to understand how many got right vs. wrong (Accuracy) but how many for each class, positive or negative.  

A Confusion Matrix is a 2x2 table (for binary classification) that plots the actual values vs. the predicted values on its axes.  Once you understand how to interpret it, it is a very easy and intuitive way to see your model's performance. 

![Confusion Matrix](images/modeleval_1.png)



$$ \text { True Negative } = \frac{T N}{T N+F P} $$

## Evaluation Metrics

1. **Accuracy:** 
2. **Precision:** 
3. **Recall:** 
4. **F1 Score:** 

![Confusion Matrix Calculations](images/modeleval_2.png)


## ROC Curve and AUC

Another methiod is to use the **ROC Curve** to determine the **Area Under the Curve** [^ROC].

An ROC curve (receiver operating characteristic curve) is a graph showing the performance of a classification model at all classification thresholds. This curve plots two parameters:

* True positive rate
* False positive rate

## References

[^CROSS][Cross-validation: evaluating estimator performance](https://scikit-learn.org/stable/modules/cross_validation.html)
[^IMB][Handling imbalanced datasets in machine learning](https://towardsdatascience.com/handling-imbalanced-datasets-in-machine-learning-7a0e84220f28)
[^ROC][Classification: ROC Curve and AUC](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc)
