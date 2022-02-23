Title: A Geltle Guide to Hyperparameter Tuning with Pipelines
Date: 2022-03-06
Modified: 2022-03-06
Status: draft
Tags: datascience, python, sklearn
Slug: hyperparameter
Authors: Brian Roepke
Summary: How to optimize the parameters of a machine learning model.
Header_Cover: images/covers/tune.jpg
Og_Image: images/covers/tune.jpg
Twitter_Image: images/covers/tune.jpg

## What is Hyperparameter Tuning?



## Pipelines

```python
pipeline.get_params()
```
```text
{'memory': None,
 'steps': [('prep',
   ColumnTransformer(transformers=[('Text', TfidfVectorizer(stop_words='english'),
                                    'text_clean'),
                                   ('Categories', TfidfVectorizer(), 'categories'),
                                   ('OHE',
                                    OneHotEncoder(dtype='int',
                                                  handle_unknown='ignore'),
                                    ['postal_code']),
                                   ('Numbers', MinMaxScaler(),
                                    ['review_count', 'text_len'])])),

...

 'clf__C': 1.0,
 'clf__class_weight': None,
 'clf__dual': False,
 'clf__fit_intercept': True,
 'clf__intercept_scaling': 1,
 'clf__l1_ratio': None,
 'clf__max_iter': 500,
 'clf__multi_class': 'auto',
 'clf__n_jobs': None,
 'clf__penalty': 'l2',
 'clf__random_state': 42,
 'clf__solver': 'lbfgs',
 'clf__tol': 0.0001,
 'clf__verbose': 0,
 'clf__warm_start': False}
```

## Grid Search

Exhastive
There are 60 permutations of the parameters.

```python
parameters = [{'clf__solver' : ['newton-cg', 'lbfgs', 'sag', 'liblinear'],
               'clf__C' : [.1, 1, 10, 100, 1000],
               'prep__Text__ngram_range': [(1, 1), (2, 2), (1, 2)]}]
```

```python
clf = LogisticRegression(random_state=42, max_iter=500)
pipeline = create_pipe(clf)
```

```python
%time grid = GridSearchCV(pipeline, 
                          parameters, 
                          scoring='f1_macro', 
                          cv=3, 
                          error_score='raise').fit(X_train, y_train)

print("Best cross-validation accuracy: {:.3f}".format(grid.best_score_))
print("Test set score: {:.3f}".format(grid.score(X_test, y_test))) 
print("Best parameters: {}".format(grid.best_params_))

log_C = grid.best_params_['clf__C']
log_solver = grid.best_params_['clf__solver']
log_ngram = grid.best_params_['prep__Text__ngram_range']
```
```text
45m 51s

Best cross-validation accuracy: 0.867
Test set score: 0.872
Best parameters: {'clf__C': 100, 'clf__solver': 'newton-cg', 'prep__Text__ngram_range': (1, 2)}
```

## Halving Search


```python
%time grid = HalvingGridSearchCV(pipeline, 
                                 parameters, 
                                 scoring='f1_macro', 
                                 cv=3, 
                                 random_state=0).fit(X_train, y_train)


print("Best cross-validation accuracy: {:.3f}".format(grid.best_score_))
print("Test set score: {:.3f}".format(grid.score(X_test, y_test))) 
print("Best parameters: {}".format(grid.best_params_))

log_C_b = grid.best_params_['clf__C']
log_solver_b = grid.best_params_['clf__solver']
log_ngram_b = grid.best_params_['prep__Text__ngram_range']
```
```text
7m 43s

Best cross-validation accuracy: 0.867
Test set score: 0.872
Best parameters: {'clf__C': 100, 'clf__solver': 'sag', 'prep__Text__ngram_range': (1, 2)}
```

## Evaluating the Results

```python
def fit_and_print(pipeline, name):
    ''' take a supplied pipeline and run it against the train-test spit 
    and product scoring results.'''
    
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    score = metrics.f1_score(y_test, y_pred, average='macro')

    print(metrics.classification_report(y_test, y_pred, digits=3))

    ConfusionMatrixDisplay.from_predictions(y_test, 
                                            y_pred, 
                                            cmap=plt.cm.Blues)
    
    plt.tight_layout()
    plt.title(name)
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(name + '.png', dpi=300) 
    plt.show; 
```

```python
clf = LogisticRegression(random_state=42, max_iter=500)
pipeline = create_pipe(clf)
fit_and_print(pipeline, 'hyper_defaults')
```
```text
              precision    recall  f1-score   support

           0      0.789     0.845     0.816      9545
           1      0.925     0.894     0.909     20370

    accuracy                          0.879     29915
   macro avg      0.857     0.869     0.863     29915
weighted avg      0.882     0.879     0.880     29915
```
![Default Settings]({static}../../images/posts/hyper_defaults.png)

```python
clf = LogisticRegression(C=log_C, solver=log_solver, random_state=42, max_iter=500)
pipeline = create_pipe(clf, log_ngram)
fit_and_print(pipeline, 'hyper_grid')
```
```text
              precision    recall  f1-score   support

           0      0.839     0.810     0.824      9545
           1      0.913     0.927     0.920     20370

    accuracy                          0.890     29915
   macro avg      0.876     0.869     0.872     29915
weighted avg      0.889     0.890     0.889     29915
```

![Default Settings]({static}../../images/posts/hyper_grid.png)

```python
clf = LogisticRegression(C=log_C_b, solver=log_solver_b, random_state=42, max_iter=500)
pipeline = create_pipe(clf, log_ngram_b)
fit_and_print(pipeline, 'hyper_halving')
```
```text
              precision    recall  f1-score   support

           0      0.838     0.810     0.824      9545
           1      0.912     0.927     0.920     20370

    accuracy                          0.890     29915
   macro avg      0.875     0.869     0.872     29915
weighted avg      0.889     0.890     0.889     29915
```
![Default Settings]({static}../../images/posts/hyper_halving.png)


## Conclusion

*If you liked what you read, [subscribe to my newsletter](https://campaign.dataknowsall.com/subscribe) and you will get my cheat sheet on Python, Machine Learning (ML), Natural Language Processing (NLP), SQL, and more. You will receive an email each time a new article is posted.*
## References

Photo by <a href="https://unsplash.com/@drewpatrickmiller?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Drew Patrick Miller</a> on <a href="https://unsplash.com/s/photos/tune?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>