Title: A Quick Introduction to Bag of Words and TF-IDF
Subtitle: How Machine Learning and Natural Language Processing Models Deal with Text
Date: 2022-01-02
Modified: 2022-01-02
Status: published
Tags: datascience, nlp
Slug: bowtfidf
Authors: Brian Roepke
Summary: How Machine Learning and Natural Language Processing Models Deal with Text
Header_Cover: images/covers/radio.jpg
Og_Image: images/covers/radio.jpg
Twitter_Image: images/covers/radio.jpg


## What is a Bag of Words

Have you ever wondered how Machine Learning (ML) deals with text when ML is based on math and statistics? I mean, the text isn't numbers after all... Right? 

Let me introduce you to the** Bag-of-Words (BoW)** model. Aside from its funny-sounding name, a BoW is a critical part of **Natural Language Processing (NLP)** and one of the building blocks of performing Machine Learning on text.

A BoW is simply an *unordered* collection of words and their frequencies (counts).  For example, let's look at the following text:

```text
"I sat on a plane and sat on a chair."

and  chair  on  plane  sat
  1      1   2      1    2
```

**Note**: The tokens (words) have to be `2` or more characters in length.

It's as simple as that. Let's look at how this was computed and what it might look like with a few more sentences, or what we commonly refer to as a **document**. First, we'll import the necessary libraries.

```python
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
```

We will be using text vectorizers from [Scikit-Learn](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction). We've imported two of them, the `CountVectorizer` which creates a BoW, and `TfidfVectorizer`, which we'll talk about a little later. Let's process a few documents in the form of a *list of strings*.

```python
corpus = [
    "Tune a hyperparameter.",
    "You can tune a piano but you can't tune a fish.",
    "Fish who eat fish, catch fish.",
    "People can tune a fish or a hyperparameter.",
    "It is hard to catch fish and tune it.",
]

vectorizer = CountVectorizer(stop_words='english') 
X = vectorizer.fit_transform(corpus) 
pd.DataFrame(X.A, columns=vectorizer.get_feature_names_out())
```
```text
   catch  eat  fish  hard  hyperparameter  like  people  piano  tune
0      0    0     0     0               1     0       0      0     1
1      0    0     1     0               0     1       0      1     1
2      1    1     3     0               0     0       0      0     0
3      0    0     1     0               1     0       1      0     1
4      1    0     1     1               0     0       0      0     1
```

We can see a little more clearly what the matrix looks like for our BoW. **Rows are documents**, and **columns are unique words**. The `CountVectorizer` comes with all sorts of in-built text preprocessing, like removing stop words which we've done here. If a sentence contains a word, it will count the number of occurrences, and if there are none, it will use a `0`. The BoW approach will put more weight on words that occur more frequently, so you must remove the stop words.

## What is TF-IDF?

We saw that the BoW model would count the occurrences and more weight on most words. An alternative method known as **TF-IDF** does just the opposite. TF-IDF stands for **Term Frequency-Inverse Document Frequency**, which nicely spells out the method it's using. Instead of giving more weight to words that occur more frequently, it gives a higher weight to words that occur **less** frequently (*across the entire corpus*). In use cases where you have more **domain-specific language** in your text, this model performs better by giving weight to these less frequently occurring words. Let's run it on the same documents as before.

Before we do inverse document frequency, let's **Term Frequency**, which will work like a BoW but give us a value for each term where the *sum of squares* of the vector (document) `= 1`. This is the same as the BoW model but normalized.

```python
vectorizer = TfidfVectorizer(stop_words='english', use_idf=False) 
X = vectorizer.fit_transform(corpus) 
df = pd.DataFrame(np.round(X.A,3), columns=vectorizer.get_feature_names_out())
df
```
```text
   catch    eat   fish  hard  hyperparameter  people  piano   tune
0  0.000  0.000  0.000   0.0           0.707     0.0  0.000  0.707
1  0.000  0.000  0.408   0.0           0.000     0.0  0.408  0.816
2  0.302  0.302  0.905   0.0           0.000     0.0  0.000  0.000
3  0.000  0.000  0.500   0.0           0.500     0.5  0.000  0.500
4  0.500  0.000  0.500   0.5           0.000     0.0  0.000  0.500
```

In the first document (`0`), we see the word `hyperparameter`, which we could consider a very domain-specific word, has the same weighting as `tune,` which occurs more frequently across the entire corpus. 

For document `2`, we can see the word `fish` has a large value because it occurs often. Now that we have our values let's look at what happens when we apply **Inverse Document Frequency**. 


```python
vectorizer = TfidfVectorizer(stop_words='english') 
X = vectorizer.fit_transform(corpus) 
df = pd.DataFrame(np.round(X.A,3), columns=vectorizer.get_feature_names_out())
df
```
```text
   catch    eat   fish   hard  hyperparameter  people  piano   tune
0  0.000  0.000  0.000  0.000           0.820   0.000  0.000  0.573
1  0.000  0.000  0.350  0.000           0.000   0.000  0.622  0.701
2  0.380  0.471  0.796  0.000           0.000   0.000  0.000  0.000
3  0.000  0.000  0.373  0.000           0.534   0.661  0.000  0.373
4  0.534  0.000  0.373  0.661           0.000   0.000  0.000  0.373
```

Let's compare the two models. In the first document, `hyperparameter` has a higher weight than tune because it occurs `50%` less than the word tune. Notice, however, that the weights are still document-dependent; `tune` does have different weights in different documents depending on each context.

For document `2`, we can see that the term `fish` has been weighted slightly less due to how often it occurs. 

## Conclusion

Hopefully, this quick overview was helpful for you in understanding BOW and TF-IDF. While they're really easy to build with libraries like **Scikit-Learn**, it is important to understand the concepts and even when one might perform better than the other. If you would like to see TF-IDF in practice, check out the post on [Clustering Text with k-Means]({filename}textclustering.md).

Check out the full code for this post on [GitHub](https://github.com/broepke/BoW_TF-IDF)

*If you liked what you read, [subscribe to my newsletter](https://campaign.dataknowsall.com/subscribe) and you will get my cheat sheet on Python, Machine Learning (ML), Natural Language Processing (NLP), SQL, and more. You will receive an email each time a new article is posted.*

## References

Photo by <a href="https://unsplash.com/@christianlue?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Christian Lue</a> on <a href="https://unsplash.com/s/photos/frequency?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
  
1. [A Gentle Introduction to the Bag-of-Words Model](https://machinelearningmastery.com/gentle-introduction-bag-words-model/)
2. [TF-IDF by Jonathan Soma](https://jonathansoma.com/lede/foundations/classes/text%20processing/tf-idf/)