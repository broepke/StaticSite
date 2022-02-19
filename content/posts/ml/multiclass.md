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



https://scikit-learn.org/stable/modules/multiclass.html#ovr-classification 


## Multi-Class Strategies

![Uncompressed Image]({static}../../images/posts/multiclass_1.png)  


```python
def create_pipe(clf):
    '''Create a pipeline for a given classifier.  The classifier needs to be an instance
    of the classifier with all parmeters needed specified.'''
    
    # Each pipeline uses the same column transformer.  
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
models = {'LogReg' : LogisticRegression(random_state=42, 
                                        class_weight='balanced', 
                                        max_iter=500),
          'RandomForest' : RandomForestClassifier(
                                        class_weight='balanced', 
                                        random_state=42),
          }

for name, model, in models.items():
    clf = model
    pipeline = create_pipe(clf)
    cv = RepeatedStratifiedKFold(n_splits=10, 
                                 n_repeats=3, 
                                 random_state=1)
    %time scores = cross_val_score(pipeline, X, y, scoring='f1_weighted', cv=cv, n_jobs=1, error_score='raise')
    print(name, ': Mean f1 Weighted: %.3f and Standard Deviation: (%.3f)' % \
        (np.mean(scores), np.std(scores)))
```
```text
CPU times: user 1min 31s, sys: 15.1 s, total: 1min 46s
Wall time: 1min 31s
LogReg : Mean f1 Weighted: 0.817 and Standard Deviation: (0.006)
CPU times: user 5min 9s, sys: 4.18 s, total: 5min 13s
Wall time: 5min 14s
RandomForest : Mean f1 Weighted: 0.769 and Standard Deviation: (0.007)
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
                                            cmap=plt.cm.YlOrBr)

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

![Uncompressed Image]({static}../../images/posts/multiclass_2.png)  

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
revs = ['This dress is gorgeous and I love it and would gladly reccomend it to all of my friends.',
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
This dress is gorgeous and I love it and would gladly reccomend it to all of my friends. = Dresses
This skirt has really horible quality and I hate it! = Bottoms
A super cute top with the perfect fit. = Tops
The most gorgeous pair of jeans I have seen. = Bottoms
this item is too little and tight. = Intimate
```

## Multi-Label Classification

```python
# Tokenize the words
df['Department Name'] = df['Department Name'].apply(word_tokenize)
```

```python
X = df[['Text_Processed', 'Department Name']]
y = df['Department Name']
```

```python
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(y)
```

```python
mlb.classes_
```
```text
array(['Bottoms', 'Dresses', 'Intimate', 'Jackets', 'Tops', 'Trend'],
      dtype=object)
```

```python
def create_pipe(clf):
    
    # Create the column transfomer
    column_trans = ColumnTransformer(
            [('Text', TfidfVectorizer(), 'Text_Processed')],
            remainder='drop') 
    
    # Build the pipeline
    pipeline = Pipeline([('prep',column_trans),
                         ('over', SMOTE(random_state=42)),
                         ('under', RandomUnderSampler(random_state=42)), 
                         ('clf', clf)])
     
    return pipeline
```

```python
models = {'Logistic Regression' : MultiOutputClassifier(LogisticRegression(max_iter=500, random_state=42)),
          'Random Forest' : MultiOutputClassifier(RandomForestClassifier(random_state=42))
          }

for name, model, in models.items():
    clf = model
    pipeline = create_pipe(clf)
    %time scores = cross_val_score(pipeline, X, y, scoring='f1_macro', cv=3, n_jobs=1, error_score='raise')
    print(name, ': Mean f1 Macro: %.3f and Standard Deviation: (%.3f)' % (np.mean(scores), np.std(scores)))
```
```text
CPU times: user 12.2 s, sys: 4.47 s, total: 16.6 s
Wall time: 10.9 s
Logistic Regression : Mean f1 Macro: 0.589 and Standard Deviation: (0.012)
CPU times: user 3min 13s, sys: 3.34 s, total: 3min 16s
Wall time: 3min 16s
Random Forest : Mean f1 Macro: 0.413 and Standard Deviation: (0.008)
```

```python
clf = MultiOutputClassifier(LogisticRegression(max_iter=500, random_state=42))

pipeline = create_pipe(clf)

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
score = metrics.f1_score(y_test, y_pred, average='macro', zero_division=0)

print(metrics.classification_report(y_test, y_pred, digits=3, zero_division=0))
```

```python
# Retreive the text lables from the MultiLabelBinarizer
pred_labels = mlb.inverse_transform(y_pred)

# Append them to the DataFrame
X_test['Predicted Labels'] = pred_labels
```

```python
# Display a random sample of them
X_test.sample(10, random_state=2)
```
```text
                                          Text_Processed Department Name  \
2356   stun color love blous color realli uniqu love ...          [Tops]   
4073   absolut ador saw onlin said next time retail s...       [Dresses]   
13905  run small short size  skirt great cute design ...       [Bottoms]   
10098             great comfi shirt long enough wear leg          [Tops]   
14467  small peopl cute concept larg realiti  size  j...       [Bottoms]   
6      cagrcoal shimmer fun ade basket hte last mintu...          [Tops]   
11381  nice vest itchi vest nice fashion stylish like...          [Tops]   
2438   comfort stylish great top older woman want sty...          [Tops]   
5256   uniqu casual winner love top pair ag stevi sho...          [Tops]   
1303   sad sack that look like wear dress sad sad sac...       [Dresses] 

2356           [Tops]           (Tops,)  
4073        [Dresses]        (Dresses,)  
13905       [Bottoms]        (Bottoms,)  
10098          [Tops]  (Intimate, Tops)  
14467       [Bottoms]                ()  
6              [Tops]                ()  
11381          [Tops]        (Jackets,)  
2438           [Tops]           (Tops,)  
5256           [Tops]           (Tops,)  
1303        [Dresses]        (Dresses,)
```

```python
filter = X_test['Predicted Labels'].apply(lambda x: len(x) > 1)
df_mo = X_test[filter]
df_mo
```
```text
                                          Text_Processed Department Name  \
17917  soft thick without bulk got mani compliment fi...          [Tops]   
11460  love bought top size medium love super comfort...          [Tops]   
10108  cute design poor materi love fact dress cotton...       [Dresses]   
12363  favorit hope love tunic isnt hope materi cute ...          [Tops]   
13795  soft top reveal nonton arm fabric super soft g...          [Tops]   
...                                                  ...             ...   
5830   good buy anoth pair bought wear christma parti...       [Bottoms]   
1074   gorgeou high qualiti figur flatter swimsuit co...      [Intimate]   
16306  pretti comfort airi top realli like design col...          [Tops]   
3703   great fit comfort flashi love top soooooo much...      [Intimate]   
3180            soft love top soft cute design great leg          [Tops]   

          Predicted Labels  
17917      (Jackets, Tops)  
11460     (Intimate, Tops)  
10108  (Dresses, Intimate)  
12363      (Jackets, Tops)  
13795     (Intimate, Tops)  
...                    ...  
5830   (Bottoms, Intimate)  
1074      (Intimate, Tops)  
16306     (Intimate, Tops)  
3703      (Intimate, Tops)  
3180      (Intimate, Tops) 
```



## Conclusion


*If you liked what you read, [subscribe to my newsletter](https://campaign.dataknowsall.com/subscribe) and you will get my cheat sheet on Python, Machine Learning (ML), Natural Language Processing (NLP), SQL, and more. You will receive an email each time a new article is posted.*

## References

Photo by <a href="https://unsplash.com/@joshstyle?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">JOSHUA COLEMAN</a> on <a href="https://unsplash.com/s/photos/multiple?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>

Search term = multiple
  