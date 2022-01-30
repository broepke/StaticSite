Title: Predict a Product Rating Using Only the Review’s Text
Subtitle: Utilize Machine Learning Classification Models on Text to Classify Product Reviews
Date: 2022-01-22
Modified: 2022-01-22
Status: draft
Tags: datascience, machine learning
Slug: classification
Authors: Brian Roepke
Summary: Utilize machine learning to automatically classify product reviews as positive or negative.
Header_Cover: images/covers/class.jpg
Og_Image: images/covers/class.jpg
Twitter_Image: images/covers/class.jpg


## What is Classification in Machine Learning?

There are two general types of supervised machine learning outcomes in their simplest form. First, you can have a regression problem, where you're trying to predict a continuous variable, such as the temperature or a stock price. The second is a classification problem where you want to predict a categorical variable such as pass/fail or spam/ham. Additionally, we can have binary classification problems that we'll cover here with only two outcomes and multi-class classification with more than two outcomes.

## Prepping the Data

You want to take several steps when preparing data for machine learning. You want to clean the data removing unwanted characters or numbers, you want to remove stop words, or words that appear too frequently, and you also should *stem*, or *lemmatize* words, which takes words such as *running* and *runs* and brings them to their root form of *run*. Additionally, you might want to create new columns or features that aid your machine learning classification process. For this example, we will use the dataset of [Women’s E-Commerce Clothing Reviews on Kaggle](https://www.kaggle.com/nicapotato/womens-ecommerce-clothing-reviews).

Before we start cleaning, let's import the data and create a few key features:

1. Since we're performing binary classification, our **target** variable needs to be `1` or `0`. In a five-star review system, we can take the `4` and `5` star reviews and make them **positive** and then let the remainder, `1`, `2`, and `3` star reviews be **negative**.
2. This particular set of reviews has both a **title* and a *body**. We can combine these two columns into a single new column called **Text**to simplify our processing.
3. As another feature in our model, we can create a new column representing the review text's **total length**.


```python
# Import the data
df = pd.read_csv("ClothingReviews.csv")

# add a column for positive or negative based on the 5 star review
df['Target'] = df['Rating'].apply(lambda c: 0 if c < 4 else 1)

# Combine the title and text into a single column
df['Text'] = df['Title'] + ' ' + df['Review Text']

# Create a new column that is the length of the next text field
df['text_len'] = df.apply(lambda row: len(row['Text']), axis = 1)
```

Next, we need to clean the text. I've created a function adapted to almost any NLP cleaning situation. Let's take a look at the text before text:

```text
' Love this dress!  it\'s sooo pretty.  i happened to find it in a store, and i\'m glad i did bc i never would have ordered it online bc it\'s petite.  i bought a petite and am 5\'8".  i love the length on me- hits just a little below the knee.  would definitely be a true midi on someone who is truly petite.'
```

```python
def process_string(text):
    
    final_string = ""
    
    # Convert the text to lowercase
    text = text.lower()
    
    # Remove punctionation
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)

    # Remove stop words and usless words
    text = text.split()
    useless_words = nltk.corpus.stopwords.words("english")
    text_filtered = [word for word in text if not word in useless_words]
    
    # Remove numbers
    text_filtered = [re.sub('\w*\d\w*', '', w) for w in text_filtered]
    
    # Stem the text with NLTK PorterStemmer
    stemmer = PorterStemmer() 
    text_stemmed = [stemmer.stem(y) for y in text_filtered]

    # Join the words back into a string
    final_string = ' '.join(text_stemmed)
    
    return final_string
```

We use the **Pandas** `apply` method to run this on our Data Frame. After applying this function, let's look at the resulting string.

```python
df['Text_Processed'] = df['Text'].apply(lambda x: process_string(x))
```

```text
'love dress sooo pretti happen find store im glad bc never would order onlin bc petit bought petit  love length hit littl knee would definit true midi someon truli petit'
```

We can see that the string is perfectly clean, free of numbers, punctions, stop words, and the words are stemmed from their most simple forms. We're ready to start building our model! 

## Testing for Imbalanced Data

We must understand if our dataset is *imbalanced* between the two classes in our Target. We can do this quickly with one line of code from Pandas. Imbalanced data is where one class has far more (or fewer) observations than the other. When we train our model, the result will be that the model will be biased towards the class with the most observations. This bias is called *overfitting* and is a common problem with machine learning.

```python
df['Target'].value_counts()
```
```text
1    17433
0     5193
Name: Target, dtype: int64
```

That is good enough to let us know that **we do have imbalanced data**. There is three times the number of positive class `1` observations versus the negative class `0`. We will have to make sure that we handle this appropriately in our model. I'll cover a couple of different ways in this article. 

## Model Selection

When building a machine learning model, a best practice is to perform what is known as **Model Selection**. Model select lets you test different algorithms on your data and determine which performs best. First, we will split our dataset into `X` and `y` datasets. `X` represents all of the features of our model, and `y` will represent the target variable. The target is the variable we're trying to predict.

```python
X = df[['Text', 'text_len']]
y = df['Target']
```

Next, we're going to use a column transformer. A column transformer allows us to preprocess data in any number of ways that are appropriate for our model. There are *many* different ways to transform your data, and I'll not cover them all here, but let me explain the two we're using.

* **TfidfVectorizer**: the TF-IDF vectorizer transforms text into numeric values. For a great descripion of this, check out my post on [BoW and TF-IDF](({filename}../nlp/bowtfidf.md)). Here we're transforming our `Text` column.
* **MinMaxScaler**: This transforms all numeric values into a range between `0` and `1`. Most ML algorithms do not handle data with a wide range of values; it's always a best practice to scale your data. You can read more about this on Scikit-Learn's [documentation](https://scikit-learn.org/stable/modules/preprocessing.html). Here we're scaling our `text_len` column.

```python
def col_trans():
    column_trans = ColumnTransformer(
            [('Text', TfidfVectorizer(), 'Text'),
             ('Text Length', MinMaxScaler(), ['text_len'])],
            remainder='drop') 
    
    return column_trans
```

Next we have a function for creating a [Pipeline](({filename}sklearnpipelines.md)). A Pipeline allows us to consistently preprocess our data and ally various additional steps in a single workflow. Let's break down what's happening below.

1. **Prep**: This is the column transformer from above. It's going to vectorize our text and scale our text length.
2. **CLF**: This is where we choose an instance of our classifier. You can see that this is passed into our function, and we do it like this so that we can test different classifiers with the same data.

```python
def create_pipe(clf):
    
    # Each pipeline uses the same column transformer.  
    column_trans = col_trans()
    
    # Create the pipleline 
    pipeline = Pipeline([('prep',column_trans),
                         ('clf', clf)])
     
    return pipeline
```

Now it's time to **Cross Validate** a couple of classifiers. Cross-validation is the process of partitioning data into *n* number of different splits, which you then validate your model against. This is so important because, in some cases of a train-test split, the observations it learns off of in the train set might not represent the observations in the test set, and therefore, you avoid this but running through different slices of the data. Read more about this on [Scikit-Learn's documentation](https://scikit-learn.org/stable/modules/cross_validation.html).

**Important**: One thing I want to bring special attention to below is [**RepeatedStratifiedKFold**](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.RepeatedStratifiedKFold.html) for cross-validation. A *Stratified* cross validator will ensure in the case of *imbalanced* data that the partitions *preserve relative class frequencies* in the split.

Finally, regarding how we're dealing with imbalanced data, we will use a classifier that supports the `class_weight` parameter. A handful of models from Scikit-Learn support this, and simply by setting the value to `balanced`, we can account for imbalanced data. There are other methods, such as SMOTE, but this is a great place to start. You can read more about [working with imbalanced data](({filename}imbalanced.md)) from my other post.

```python
models = {'LogReg' : LogisticRegression(random_state=42, 
                                        class_weight='balanced', 
                                        max_iter=500),
          'RandomForest' : RandomForestClassifier(
                                        class_weight='balanced', 
                                        random_state=42)}

for name, model, in models.items():
    clf = model
    pipeline = create_pipe(clf)
    cv = RepeatedStratifiedKFold(n_splits=10, 
                                 n_repeats=3, 
                                 random_state=1)
    scores = cross_val_score(pipeline, X, y, 
                             scoring='f1_weighted', cv=cv, 
                             n_jobs=-1, error_score='raise')
    print(name, ': Mean f1 Weighted: %.3f and StdDev: (%.3f)' % \
        (np.mean(scores), np.std(scores)))
```

```text
LogReg : Mean f1 Weighted: 0.879 and Standard Deviation: (0.005)
RandomForest : Mean f1 Weighted: 0.845 and Standard Deviation: (0.006)
```

In the above function, you can see that scoring is done with `f1_weighted`. Choosing the right metric is a whole discussion that is critical to understand. I've written about how to choose the right [evaluation metric](({filename}modeleval.md)). 

Here is a quick explanation of why I chose this metric. First, we have Imbalanced data, and we **never** want to use `accuracy` as our metric. Accuracy on imbalanced data will give you a false sense of success, but practice will only tell about the class with more observations. In some projects, you might want to make sure you have no false positives, and in others, you may want to ensure you have a better prediction of true positives. 

Second, we don't prefer to predict positive reviews versus negative reviews in this case, so I've chosen the `F1` score. `F1` by definition, is the harmonic mean of Precision and Recall combining them into a single metric. However, there is also a way to tell this metric to score imbalanced data with the `weighted` flag. As the [Sciki-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html) documentation states:

>*Calculate metrics for each label and find their average weighted by support (the number of true instances for each label). This alters ‘macro’ to account for label imbalance; it can result in an F-score between precision and recall.*

Based on these results, we can see that the `LogisticRegression` classifier performs slightly better and is much faster. Therefore we can move forward and train our model with it.

Again, please read my full explanation of [evaluation metric](({filename}modeleval.md)) to give you a better sense of which one to use and when.

## Model Training and Validation

We're finally here! It's time to train our final model and validate it. We'll split our data into **training** and **test** data sets since we didn't do this yet when we used Cross-Validation above. You never want to train your data on *all* of your data, but rather leave a portion out for testing. Whenever a model has seen data during training, it will know that data and cause *overfitting*. Overfitting is a problem where a model is too good at predicting the data it has seen and is not generalizable to new data.

```python
# Make training and test sets 
X_train, X_test, y_train, y_test = train_test_split(X, 
                                                    y, 
                                                    test_size=0.33, 
                                                    random_state=53)
```

Next, a quick function will fit our model and evaluate it with both a `classification_report` and a Confusion Matrix. I believe it's critical to run the classification report at a minimum, and it will show you each of your key evaluation metrics and tell you how the model performed. The Confusion Matrix is a great way to visualize the results.

```python
def fit_and_print(pipeline, name):
    
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    print(metrics.classification_report(y_test, y_pred, digits=3))
        
    ConfusionMatrixDisplay.from_predictions(y_test, 
                                            y_pred, 
                                            cmap=plt.cm.YlOrBr)

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('predicted label')
    plt.tight_layout()
    plt.savefig('classification_1.png', dpi=300)  
```

```python
clf = LogisticRegression(random_state=42, 
                         class_weight='balanced', 
                         max_iter=500)
pipeline = create_pipe(clf)
fit_and_print(pipeline, 'Logistic Regression')
```
```text
              precision    recall  f1-score   support

           0      0.675     0.850     0.752      1715
           1      0.951     0.878     0.913      5752

    accuracy                          0.872      7467
   macro avg      0.813     0.864     0.833      7467
weighted avg      0.888     0.872     0.876      7467
```

![Confusion Matrix]({static}../../images/posts/classification_1.png)  

The results are in! The classification report shows us everything we need. Because we said we don't necessarily want to optimize for the positive or negative class, we will use the `f1_score` column. We can see the `0` class performed at `0.752` and the `1` class at `0.913`. Whenever you have imbalanced data, you can expect that the larger class will perform better, but you can use some of the above steps to increase the model's performance.

## Testing on New Data

Now for a demonstration of what's truly the important part. How well does your model predict new observations it has never seen before? In production, this would be very different, but we can simulate it by creating a few new reviews for a quick example. I've also created a function that transforms a list of strings into the properly formatted dataframe with cleaned text and the `text_len` column.

```python
def create_test_data(x):
    
    x = process_string(x)
    length = len(x)
    
    d = {'Text' : x,
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
print('Returns 1 for Positive reviews and 0 for Negative reviews:','\n')
for rev in revs:
    c_res = pipeline.predict(create_test_data(rev))
    print(rev, '=', c_res)
```

```text
Returns 1 for Positive reviews and 0 for Negative reviews: 

This dress is gorgeous and I love it and would gladly reccomend it to all of my friends. = [1]
This skirt has really horible quality and I hate it! = [0]
A super cute top with the perfect fit. = [1]
The most gorgeous pair of jeans I have seen. = [1]
this item is too little and tight. = [0]
```


## Conclusion


All of the code for this post is available here in [GitHub](https://github.com/broepke/Classification)

*If you liked what you read, [subscribe to my newsletter](https://campaign.dataknowsall.com/subscribe) and you will get my cheat sheet on Python, Machine Learning (ML), Natural Language Processing (NLP), SQL, and more. You will receive an email each time a new article is posted.*

## References

Photo by <a href="https://unsplash.com/@anniespratt?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Annie Spratt</a> on <a href="https://unsplash.com/s/photos/classify?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
  
