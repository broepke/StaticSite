Title: Noun Phrase Chunking
Date: 2021-12-18
Modified: 2021-12-18
Status: draft
Tags: datascience, nlp
Slug: nounphrase
Authors: Brian Roepke
Summary: Beyond Parts of Speech Tagging to Noun Phrase Chunking.
Header_Cover: images/covers/orangeneon.jpg
Og_Image: images/covers/orangeneon.jpg
Twitter_Image: images/covers/orangeneon.jpg

## What is Noun Phrase Chunking?


```python
import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("Five words in orange neon")
for chunk in doc.noun_chunks:
    print(chunk.text)
```
```text
Five words
orange neon
```


## References

Photo by <a href="https://unsplash.com/@kylry?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Kyle  Ryan</a> on <a href="https://unsplash.com/s/photos/phrases?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>

[^SPACY]: [Spacy: Industrial-Strength Natural Language Processing](https://spacy.io)
