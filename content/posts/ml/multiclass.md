Title: Go Beyond Binary Classification with Multi-Class and Multi-Label Models
Date: 2022-02-06
Modified: 2022-02-06
Status: draft
Tags: datascience, machine learning
Slug: multiclass
Authors: Brian Roepke
Summary: Utilize machine learning to automatically classify data
Header_Cover: images/covers/multi.jpg
Og_Image: images/covers/multi.jpg
Twitter_Image: images/covers/multi.jpg

## What is Multi-Class and Multi-Label Classification?

Often when you start learning about classification problems in Machine Learning you start off with [binary classification]({filename}classification.md).  This is the case where there are only two possible outcomes such as spam or not spam, fraud or not fraud, and so on.  Moving beyond that we have **mutti-class** and **multi-label** classification.  Let's start by explaining each one.

**Multi-Class Classification** is where you have more than two categories in your target variable (`y`).  For example, you could have *small*, *medium*, *large*, and , *xlarge* or you might have a rating system based on one to five stars.  Each of these levels can be considered a class as well.  The objective of this strategy is to **predict a single class** out of the available classes.

**Multi-Label Classification** is slightly different.  Here you have more than two categories available as well, but instead of chosing only a single class, the objective of this strategy is to **predict multiple classes** when applicable.  This strategy is useful when you have multiple categories that can be related to each other.  One of the best examples I've seen is when this is used in a tagging system.  For example the way that medium articles can have multiple tags assocaited with them.  This article migh thave `machine learning`, `data science`, and `python` as tags.  

Next lets dig into multi-class strategies.
## Multi-Class Strategies

Strategies are how you approach instructing the classifier to handle more than two classes which may affect performance both in terms of **generalization** or compute resources.  Generalization referes to how well the classifier works on unseen data in the future, this is the opposite of *overfitting*. Check out the Scikit-Learn [documentation](https://scikit-learn.org/stable/modules/multiclass.html#ovr-classification) for more information.

The **One-vs-Rest** or (OVR) which is also called **One-vs-All** (OVA) strategy fits a single classifier for each class which is fitted agasint all other classes.  This essentially is splitting the multi-class problem into a set of binary classification problems. This tends to perform well because there are `n` classifiers for `n` classes.  This is the most common strategy and you can start here on your journey.  What this looks like in practice is essentially this:

* **Binary 1:** small vs (medium, large, xlarge)
* **Binary 2:** medium vs (small, large, xlarge)
* **Binary 3:** large vs (small, medium, xlarge)
* **Binary 4:** xlarge vs (small, medium, large)

OVR tends to **not scale** well if you have a very **large number** of classes.  One-vs-One might be better.  Let's talk about that next.

The **One-vs-One** (OVO) strategy fits a single classifier for each pair of classes. Here is what that looks like:

* **Binary 1:** small vs medium
* **Binary 2:** small vs large
* **Binary 3:** small vs. xlarge
* **Binary 4:** medium vs large
* **Binary 5:** medium vs xlarge
* **Binary 6:** large vs xlarge

While the [compute complexity](https://en.wikipedia.org/wiki/Big_O_notation) is higher than the OVR strategy, it can be advantageous when you have a large number of classes because each of the binary classifiers is fit on a smaller subset of the data, where the OVR strategy is fit on the entire dataset for each classifier.

Finally for **multi-label** classification there is the `MultiOutputClassifier`.  Similar to **OVR**, this fits a classifier for each class, however as opposed to a single predicted output, this can, if applicable, output multiple classes for a single prediction.

**Note:** Specifially for Scikit-Learn all classifiers are multiclass capable.  You can use these strategies to further refine the performance of them.

![Multiclass Types]({static}../../images/posts/multiclass_1.png)  


```python
def create_pipe(clf):
    
    column_trans = ColumnTransformer(
            [('Text', TfidfVectorizer(), 'Text_Processed'),
             ('Text Length', MinMaxScaler(), ['text_len'])],
            remainder='drop') 
    
    pipeline = Pipeline([('prep',column_trans),
                         ('clf', clf)])
     
    return pipeline
```

```python
X = df[['Text_Processed', 'text_len']]
y = df['Department Name']
y.value_counts()
```
```text
Tops        10048
Dresses      6145
Bottoms      3660
Intimate     1651
Jackets      1002
Trend         118
Name: Department Name, dtype: int64
```

```python
le = LabelEncoder()
y = le.fit_transform(y)
```

```python
le.classes_
```
```text
array(['Bottoms', 'Dresses', 'Intimate', 'Jackets', 'Tops', 'Trend'],
      dtype=object)
```





```python
# Make training and test sets 
X_train, X_test, y_train, y_test = train_test_split(X, 
                                                    y, 
                                                    test_size=0.33, 
                                                    random_state=53)
```

```python
def fit_and_print(pipeline, name):
    ''' take a supplied pipeline and run it against the train-test spit 
    and product scoring results.'''
    
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    print(metrics.classification_report(y_test, y_pred, digits=3))
    
    ConfusionMatrixDisplay.from_predictions(y_test, 
                                            y_pred, 
                                            cmap=plt.cm.YlGn)

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
```

```python
clf = LogisticRegression(random_state=42, 
                         class_weight='balanced', 
                         max_iter=500)
pipeline = create_pipe(clf)
fit_and_print(pipeline, 'Multiclass')
```
```text
              precision    recall  f1-score   support

           0      0.785     0.855     0.818      1193
           1      0.905     0.844     0.874      2037
           2      0.439     0.581     0.500       527
           3      0.551     0.794     0.650       315
           4      0.909     0.818     0.861      3361
           5      0.022     0.061     0.033        33

    accuracy                          0.810      7466
   macro avg      0.602     0.659     0.623      7466
weighted avg      0.836     0.810     0.820      7466
```

![Confusion Matrix]({static}../../images/posts/multiclass_2.png)  

## Train on Custom Data

```python
def create_test_data(x):
    
    x = process_string(x)
    length = len(x)
    
    d = {'Text_Processed' : x,
        'text_len' : length}

    df = pd.DataFrame(d, index=[0])
    
    return df
```

```python
revs = ['This dress is gorgeous and I love it.',
        'This skirt has really horible quality and I hate it!',
        'A super cute top with the perfect fit.',
        'The most gorgeous pair of jeans I have seen.',
        'this item is too little and tight.']
```

```python
for rev in revs:
    c_res = pipeline.predict(create_test_data(rev))
    print(rev, '=', le.classes_[c_res[0]])
```
```text
This dress is gorgeous and I love it. = Dresses
This skirt has really horible quality and I hate it! = Bottoms
A super cute top with the perfect fit. = Tops
The most gorgeous pair of jeans I have seen. = Bottoms
this item is too little and tight. = Intimate
```

## Multi-Label Classification

```python
# Tokenize the words
df['Class Name'] = df['Class Name'].apply(word_tokenize)
X = df[['Text_Processed', 'Department Name']]
y = df['Class Name']
```

```python
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(y)
mlb.classes_
```
```text
array(['Blouses', 'Dresses', 'Fine', 'Intimates', 'Jackets', 'Jeans',
       'Knits', 'Layering', 'Legwear', 'Lounge', 'Outerwear', 'Pants',
       'Shorts', 'Skirts', 'Sleep', 'Sweaters', 'Swim', 'Trend', 'gauge'],
      dtype=object)
```

```python
def create_pipe(clf):
    
    # Create the column transfomer
    column_trans = ColumnTransformer(
            [('Text', TfidfVectorizer(), 'Text_Processed'),
             ('Categories', OneHotEncoder(handle_unknown="ignore"), 
              ['Department Name'])],
            remainder='drop') 
    
    # Build the pipeline
    pipeline = Pipeline([('prep',column_trans),
                         ('clf', clf)])
     
    return pipeline
```



```python
clf = MultiOutputClassifier(LogisticRegression(max_iter=500, 
                                               random_state=42))

pipeline = create_pipe(clf)

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
score = metrics.f1_score(y_test, 
                         y_pred, 
                         average='macro', 
                         zero_division=0)

print(metrics.classification_report(y_test, 
                                    y_pred, 
                                    digits=3, 
                                    zero_division=0))
```

```python
# Retreive the text lables from the MultiLabelBinarizer
pred_labels = mlb.inverse_transform(y_pred)
# Append them to the DataFrame
X_test['Predicted Labels'] = pred_labels

filter = X_test['Predicted Labels'].apply(lambda x: len(x) > 1)
df_mo = X_test[filter]
df_mo.sample(10, random_state=24)
```
```text
                 Text_Processed Department Name         Predicted Labels
12561  cute summer blous top...            Tops         (Blouses, Knits)
15309  awesom poncho back ev...            Tops            (Fine, gauge)
6672   great sweater true fo...            Tops  (Fine, Sweaters, gauge)
4446   love top love fabric ...            Tops         (Blouses, Knits)
10397  love alway pilcro pan...         Bottoms           (Jeans, Pants)
14879  love shirt perfect fi...            Tops         (Blouses, Knits)
5948   simpl stylish top jea...            Tops         (Blouses, Knits)
16643  tri youll love beauti...            Tops  (Fine, Sweaters, gauge)
17866  qualiti sweater beaut...            Tops  (Fine, Sweaters, gauge)
22163  cute top got top mail...            Tops         (Blouses, Knits)
```



## Conclusion


The full code for this article is available on [GitHub](https://github.com/broepke/Classification)


*If you liked what you read, [subscribe to my newsletter](https://campaign.dataknowsall.com/subscribe) and you will get my cheat sheet on Python, Machine Learning (ML), Natural Language Processing (NLP), SQL, and more. You will receive an email each time a new article is posted.*

## References

Photo by <a href="https://unsplash.com/@judithgirardmarczak?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">judith girard-marczak</a> on <a href="https://unsplash.com/s/photos/multicolor?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
  

Search term = multicolor
  