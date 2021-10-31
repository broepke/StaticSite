Title: Evaluating Models with a Confusion Matrix
Date: 2021-11-07
Modified: 2021-11-07
Category: SQL
Tags: datascience, ml, machine learning, confusion-matrix
Slug: modeleval
Authors: Brian Roepke
Summary: How to evaluate models using a confusion matrix and when to use different metrics.
Header_Cover: images/cranes_night.jpg

## Model Evaluation for Binary Classification

Understanding how to evaluate models is a critical part of any Machine Learning (ML) project.  Many times when we're starting with ML or when having conversations with people that aren't as well versed in ML, the term **Accuracy** is thrown out as a generalization of the model's performance.  The problem with generally talking about the **Accuracy** is that it specifically refers to the overall performance of the model's ability to predict both the positive or the negative classes in the dataset.

While **Accuracy** is acceptable for model performance when your dataset is perfectly balanced (equal positive and negative classes), the reality is that this is rarely the case.  There are methods to deal with imbalanced data, which I'll talk about later, but for now, let's understand how to interpret the results of a model's performance properly.

## Interpreting a Confusion Matrix

After a model is trained and tested on data (Scikit-Learn has a great write-up of this process[^CROSS]), you can use a Confusion Matrix to give a view of how many observations the model misclassified.  The trick to this is not just to understand how many got right vs. wrong (Accuracy) but how many for each class, positive or negative.  

A Confusion Matrix is a 2x2 table (for binary classification) that plots the actual values vs. the predicted values on its axes.  Once you understand how to interpret it, it is an easy and intuitive way to see your model's performance. 

![Confusion Matrix](images/modeleval_1.png)  

*Image Credit: Baptiste Rocca[^IMB]*

See the `Scikit-Learn` documentation[^CM] for how to display a Confusion Matrix.

## Evaluation Metrics

1. **Accuracy:** This is the percentage of observations that the model correctly predicted across both classes.  Be very careful with imbalanced data.  You can have very high Accuracy, but the performance of the minority class can be horrible.
2. **Precision:** Tells you how reliable the prediction is for the class.  e.g., when the precision score is high, and the model predicts the class, you can trust it is correct.
3. **Recall:** Tells you how well the model can predict the class.  A high recall with low Precision means that it is performing well in the class but may include other classes in the results.
4. **F1 Score:** Calculates the harmonic mean of Precision and Recall combining them into a single metric.

The following image is the best way that I've seen to illustrate how each calculation is performed.  It can also help you, once you understand what you're trying to optimize for, which type of metric you should use.

For example, if you're looking to minimize False Positives for Class 1, then Class 1 Recall is the right metric for you (*Dark Orange and Dark Blue in the Image*).

![Confusion Matrix Calculations](images/modeleval_2.png)  

*Image Credit: Baptiste Rocca[^IMB]*

## Optimize for the Outcome You Want

A critical part of picking the right evaluation metric is to decide what is the most important outcome you want.  I think of this broken down into three things:

1. **Minimize False Positives:** A use case for this might be a spam filter.  Ideally, you never want to mark a real message as spam and have it filed into a spam folder.  The potential for a user to miss an important message is high; therefore, you want to reduce false positives and choose a model with *high Precision*.
2. **Minimize False Negatives:** The best example here for me is medical screening.  It would be incredibly bad if the algorithm had a false negatives with the patient, but they were actually sick.  It would be best to flag potential issues and have an expert follow up.  In this case, you want to focus on a *high Recall*.
3. **Both:** If your use case doesn't have a bias to one or the other, then choose *F1* for a balanced metric for both Precision and Recall.


Hopefully, this helps you better understand how to interpret a confusion matrix and choose the best evaluation metric for your use case!

## References

[^CROSS]: [Cross-validation: evaluating estimator performance](https://scikit-learn.org/stable/modules/cross_validation.html)  
[^IMB]: [Handling imbalanced datasets in machine learning](https://towardsdatascience.com/handling-imbalanced-datasets-in-machine-learning-7a0e84220f28)  
[^ROC]: [Classification: ROC Curve and AUC](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc)  
[^METRIC]: [Performance Metrics: Confusion matrix, Precision, Recall, and F1 Score](https://towardsdatascience.com/performance-metrics-confusion-matrix-precision-recall-and-f1-score-a8fe076a2262) 
[^CM]: [How to display a Confusion Matrix](https://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html)
