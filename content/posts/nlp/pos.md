Title: Part of Speech Tagging
Date: 2021-12-04
Modified: 2021-12-04
Status: draft
Tags: datascience, nlp
Slug: pos
Authors: Brian Roepke
Summary: How to leverage NLP to tag words with its Part of Speech
Header_Cover: images/covers/speech.jpg
Og_Image: images/covers/speech.jpg
Twitter_Image: images/covers/speech.jpg

## What is a Part of Speech?

Part of Speech (POS) is a way to describe the grammatical function of a word. In Natural Language Processing (NLP), POS is an essential building block of language models and interpreting text. While POS tags are used in higher-level functions of NLP, it's important to understand them on their own, and it's possible to leverage them for useful purposes in your text analysis.

> There is a hierarchy of tasks in NLP (see [Natural language processing](https://en.wikipedia.org/wiki/Natural_language_processing#Major_tasks_in_NLP) for a list). At the bottom are sentence and word segmentation. POS tagging builds on top of that, and phrase chunking builds on top of POS tags. These tags, in turn, can be used as features for higher-level tasks such as building parse trees, which can, in turn, be used for Named Entity Resolution, Coreference Resolution, Sentiment Analysis, and Question Answering [^QUORA].

There are eight different parts of speech in English that are commonly defined [^POS].

1. **Noun**: A noun is the name of a person, place, thing, or idea.
2. **Pronoun**: A pronoun is a word used in place of a noun.
3. **Verb**: A verb expresses action or being.
4. **Adjective**: An adjective modifies or describes a noun or pronoun.
5. **Adverb**: An adverb modifies or describes a verb, an adjective, or another adverb.
6. **Preposition**: A preposition is a word placed before a noun or pronoun to form a phrase modifying another word in the sentence.
7. **Conjunction**: A conjunction joins words, phrases, or clauses.
8. **Interjection**: An interjection is a word used to express emotion. 
9. **Determiner (Article)**: A determiner is a word that indicates several objects or people. (These are not always considered a POS but are often included in POS tagging libraries.)

## The Basics of POS Tagging

Let's start with some simple examples of POS tagging with three common Python libraries: NLTK [^NLTK], TextBlob [^BLOB], and Spacy [^SPACY]. We'll do the absolute basics for each and compare the results.

Start by importing all the needed libraries.

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import nltk

from textblob import TextBlob
from textblob.taggers import PatternTagger

import spacy
```

For our examples, we'll use two sentences with a common word (book) to test how well the POS taggers work in context.

* *Please book my flight to California*
* *I read a very good book*
### NLTK

Let's start with the most common library for NLP in Python; the **Natural Language Toolkit** or **NLTK**.

```python
tokenized_sent = nltk.sent_tokenize("Please book my flight to California")
[nltk.pos_tag(nltk.word_tokenize(word)) for word in tokenized_sent]
```
```text
[[('Please', 'NNP'),
  ('book', 'NN'),
  ('my', 'PRP$'),
  ('flight', 'NN'),
  ('to', 'TO'),
  ('California', 'NNP')]]
```

```python
tokenized_sent = nltk.sent_tokenize("I read a very good book")
[nltk.pos_tag(nltk.word_tokenize(word)) for word in tokenized_sent]
```
```text
[[('I', 'PRP'),
  ('read', 'VBP'),
  ('a', 'DT'),
  ('very', 'RB'),
  ('good', 'JJ'),
  ('book', 'NN')]]
```

What we notice here is that for the most part, **NLTK** properly recognizes the word in context; however, a few errors such as *Please* is tagged as a *Proper Noun (NNP)* and *book* is tagged as a *Noun (NN)* in our first sentence when it should be a *Verb (VB)*. 

**Note:** For a list of what the tags mean, see [Penn Treebank Project](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html).

### TextBlob

Let's try another library called **TextBlob** which provides a simple API for diving into standard natural language processing (NLP) tasks [^BLOB]. It's a very good Pythonic implementation of an NLP library and simplifies some of the common NLP tasks. Much of what **TextBlob** does is *wrap NLTK* and other popular NLP libraries to make them easier to use.

```python
blob = TextBlob("Please book my flight to California", pos_tagger=PatternTagger())
blob.tags
```
```text
[('Please', 'VB'),
 ('book', 'NN'),
 ('my', 'PRP$'),
 ('flight', 'NN'),
 ('to', 'TO'),
 ('California', 'NNP')]
```

```python
blob = TextBlob("I read a very good book", pos_tagger=PatternTagger())
blob.tags
```
```text
[('I', 'PRP'),
 ('read', 'VB'),
 ('a', 'DT'),
 ('very', 'RB'),
 ('good', 'JJ'),
 ('book', 'NN')]
```

Notice the use of `PatternTagger` in the initialization of the Blob. The default is to use NLTK's tagger, yielding the same results as above. This allows us to try a different POS Tagger and check its performance. We can see that **TextBlob** correctly identifies *Please* as a *Verb* this time but still misses *Book* as a *Verb* in the first sentence.

### Spacy

**Spacy** is the most modern and advanced of the three of these. It's incredibly robust for tons of NLP tasks and allows for customization if more power is needed. This is currently my favorite NLP library, and let's check it out with our sentences.

```python
# Spacy Version
doc = nlp("Please book my flight to California")
for token in doc:
    print(token.text, token.pos_)
```
```text
Please INTJ
book VERB
my PRON
flight NOUN
to ADP
California PROPN
```

```python
# Spacy Version
doc = nlp("I read a very good book")
for token in doc:
    print(token.text, token.pos_)
```
```text
I PRON
read VERB
a DET
very ADV
good ADJ
book NOUN
```

We see here that **Spacy** correctly tagged all of our words, and it identified *Please* like an *Interjection* [^PLEASE] as opposed to a *Verb*, which is more accurate and also identified *Book* as a *Verb* in the first sentence.

Each of these libraries has its pros and cons. I believe you should start with **NLTK** to understand how it works, especially since it has so much robust support for different lexicons. **TextBlob** is great when you want simplicity across several NLP tasks, and **Spacy** when you want the most robust.

## References

Photo by <a href="https://unsplash.com/@apellaes?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Alexandre Pellaes</a> on <a href="https://unsplash.com/s/photos/conferences?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>

[^QUORA]: [What are the applications of tagging in NLP?](https://www.quora.com/What-are-the-applications-of-tagging-in-NLP)
[^POS]: [The Eight Parts of Speech](https://www.butte.edu/departments/cas/tipsheets/grammar/parts_of_speech.html)
[^WIKI]: [Part of Speech on Wikipedia](https://en.wikipedia.org/wiki/Part_of_speech)
[^NLTK]: [NLTK: Natural Language Toolkit](https://www.nltk.org)
[^BLOB]: [TextBlob: Simplified Text Processing](https://textblob.readthedocs.io/en/dev/)
[^SPACY]: [Spacy: Industrial-Strength Natural Language Processing](https://spacy.io)
[^PLEASE]: [Should I use a comma before or after “please” in a sentence?](https://prowritingaid.com/grammar/1008092/Should-I-use-a-comma-before-or-after-“please”-in-a-sentence)
