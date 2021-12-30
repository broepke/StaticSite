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


## Twitter Data


[Tweet Extraction Notebook](https://github.com/broepke/SentimentAnalysis/blob/main/twitter.ipynb)


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

![Swift with TextBlob]({static}../../images/posts/sentiment_swift_blob.png)  

![Maxwell with TextBlob]({static}../../images/posts/sentiment_maxwell_blob.png)  

## Social Media Sentiment Analysis with Vader


```python
# Add the polarity scores
swift['vader'] = swift['text'].apply(lambda x: sid.polarity_scores(x))
```
```text
{'neg': 0.0, 'neu': 0.793, 'pos': 0.207, 'compound': 0.7184}
```



```python
# Extract only the compound score value
swift['compound'] = swift['vader'].apply(lambda score_dict: score_dict['compound'])
swift.head()
```

Vader is trained for short texts.

![Swift with Vader]({static}../../images/posts/sentiment_swift_vader.png)  

![Maxwell with Vader]({static}../../images/posts/sentiment_maxwell_vader.png)  

## Conclusion


[GitHub](https://github.com/broepke/SentimentAnalysis)


## References

Photo by <a href="https://unsplash.com/@bel2000a?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Belinda Fewings</a> on <a href="https://unsplash.com/s/photos/sentiment?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
  