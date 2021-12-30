Title: Sentiment Analysis
Date: 2021-01-04
Modified: 2021-01-04
Status: draft
Tags: datascience, nlp
Slug: sentiment
Authors: Brian Roepke
Summary: Sentiment Analysis of Text utilizing multiple frameworks.
Header_Cover: images/covers/grass_love.jpg
Og_Image: images/covers/grass_love.jpg
Twitter_Image: images/covers/grass_love.jpg

## What is Sentiment Analysis?

Sentiment analysis helps understand the tone of questions posted, positive, negative, or neutral. Capturing sentiment can help organizations better understand the Voice of Customer (VOC) and even direct product development to improve functionality [^IJCA].  Often times sentimen analysis is lexicon based, meaning it simply references words that are tagged by humans as positive, negative, or neutral.  There are more advanced models avaialble such as BERT, which was opensourced by Google in 2018 [^BERT].  This post will cover the more traditional lexicon based approach, we'll take a look at the deep learning models at a later time.

## Twitter Data

For this example we're going to use data extracted from Twitter.  Twitter is an excellent source for **Voice of Customer** (VOC) analysis.  You can search a product name, a hastag, mentions, or a company name.  For Python we can use the [Tweepy](https://docs.tweepy.org/en/stable/#) API wrapper of the [Twitter API](https://developer.twitter.com/en).  

The code I used to extract this data is available here: [Tweet Extraction Notebook](https://github.com/broepke/SentimentAnalysis/blob/main/twitter.ipynb)


## Sentiment Analysis with TexBlob


```python
def get_sentiment(x):
    '''using TextBlob, get the sentiment score for a given body of text'''
    blob = TextBlob(x)
    return blob.sentiment.polarity
```

```python
swift['blob'] = swift['text'].apply(lambda x: get_sentiment(x))
swift.head()
```
```text
0  RT @TSwiftFTC: 🥇 According to @HITSDD, Taylor ...   1.000000
1  RT @taylorr_media: Taylor Swift - All Too Well...    0.000000
2  Taylor swift and ed sheeran music mainly. And ...    0.166667
3  RT @soitgoes: taylor swift didn't write:...          0.200000
4  Suporte list: Nial Horan, Demi Lovato, Taylor ...    0.000000
```




Works with longer text, simple to use, general solution.

```python
# Get rid of neutral sentiment
filter = swift['blob'] != 0
swift = swift[filter]
```


```python
sns.histplot(swift, x='blob', color="#7C8C58", bins=10)
plt.title("Taylor Swift Sentiment Distribution with TextBlob")
plt.xlabel("Sentiment")
plt.ylabel("")
```


![Swift with TextBlob]({static}../../images/posts/sentiment_swift_blob.png)  

![Maxwell with TextBlob]({static}../../images/posts/sentiment_maxwell_blob.png)  

## Social Media Sentiment Analysis with Vader

Tools tuned explicitly to social media are emerging that understand how to deal with the language patterns used in social media and even handling items such as emoji characters in text. One such is VADER1 (Valence Aware Dictionary and sEntiment Reasoner) library [^VADER].

Vader is trained for short texts.

```python
# Add the polarity scores
swift['vader'] = swift['text'].apply(lambda x: sid.polarity_scores(x))
```

The resulting column is actually a dictionary of different key-value pairs.  The one that most closely represents the TextBlob sentiment is `compound`.  

```text
{'neg': 0.0, 'neu': 0.793, 'pos': 0.207, 'compound': 0.7184}
```

We can extract that key-value pair with the following function applied to our dataframe:

```python
# Extract only the compound score value
swift['compound'] = swift['vader'].apply(lambda score_dict: score_dict['compound'])
swift.head()
```

And finally we can visualize the distribution of the sentiment scores.

![Swift with Vader]({static}../../images/posts/sentiment_swift_vader.png)  

![Maxwell with Vader]({static}../../images/posts/sentiment_maxwell_vader.png)  

## Conclusion


[GitHub](https://github.com/broepke/SentimentAnalysis)


## References

Photo by <a href="https://unsplash.com/@bel2000a?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Belinda Fewings</a> on <a href="https://unsplash.com/s/photos/sentiment?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>

[^WIKI]: [Sentiment analysis on Wikipedia](https://en.wikipedia.org/wiki/Sentiment_analysis)
[^IJCA]: [Approaches, Tools and Applications for Sentiment Analysis Implementation](https://www.ijcaonline.org/research/volume125/number3/dandrea-2015-ijca-905866.pdf)
[^BERT]: [Open Sourcing BERT: State-of-the-Art Pre-training for Natural Language Processing](https://ai.googleblog.com/2018/11/open-sourcing-bert-state-of-art-pre.html)
[^VADER]: [VADER-Sentiment-Analysis on GitHub](https://github.com/cjhutto/vaderSentiment)