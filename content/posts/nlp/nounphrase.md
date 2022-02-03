Title: A Quick Guide to Noun Phrase Chunking
Date: 2021-12-18
Modified: 2021-12-18
Status: published
Tags: datascience, nlp
Slug: nounphrase
Authors: Brian Roepke
Summary: Noun Phrase Chunking in NLTK and sPacy
Header_Cover: images/covers/orangeneon.jpg
Og_Image: images/covers/orangeneon.jpg
Twitter_Image: images/covers/orangeneon.jpg

## What is Noun Phrase Chunking?

In the last post, I covered [Part of Speech Tagging]({filename}pos.md), which is the process of tagging words with their grammatical parts. Here I will cover **Noun Chunking** or **Noun Phrase Chunking**, or **Base Noun Phrases** [^SPACY]. Chunking builds upon these grammatical parts to identify groups of words that go together to form symbolic meaning. This can be an adjective that goes along with a noun or a group of nouns related to each other. Below is a simple example using Spacy to demonstrate how it works.

```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Five Words in Orange Neon")
for chunk in doc.noun_chunks:
    print(chunk.text)
```
```text
Five Words
Orange Neon
```

In this simple five-word sentence, we can see how it identified **Five Words** and **Orange Neon** as the chunks. 

For this post, we'll take this blob of text about Chatbots[^WIKI] and compare both Spacy's and NLTK's methods for chunking:

>*A chatbot (also known as a talkbot, chatterbot, Bot, IM bot, interactive agent, or Artificial Conversational Entity) is a computer program or an artificial intelligence which conducts a conversation via auditory or textual methods. Such programs are often designed to convincingly simulate how a human would behave as a conversational partner, thereby passing the Turing test. Chatbots are typically used in dialog systems for various practical purposes including customer service or information acquisition. Some chatterbots use sophisticated natural language processing systems, but many simpler systems scan for keywords within the input, then pull a reply with the most matching keywords, or the most similar wording pattern, from a database.*

## Noun Phrase Chunking with NLTK

Let's start with NLTK. I mentioned in the post on [Part of Speech Tagging]({filename}pos.md) that having a solid understanding of NLTK will give you a good foundation in Natural Language Processing. Some methods require a little more effort to implement than other NLP libraries; however, NLTK is a solid foundation to build upon.

To chunk with NLTK, you use `RegEx` to pull out the different chunks that you wish to work with. It can take a little bit of experimentation, but it's quite flexible overall. First, let's import the needed parts of NLTK.

```python
import nltk
from nltk.tokenize import word_tokenize
from nltk import word_tokenize, pos_tag
```

And next, we'll set up a function that will help us extract the different chunks based on a `RegEx` pattern that we want to identify.

```python
def reg_chunker(sent, expression):

    sent = pos_tag(word_tokenize(sent))
    cp = nltk.RegexpParser(expression)
    chunked = cp.parse(sent)

    for chunk in chunked.subtrees(filter=lambda t: t.label() == 'NP'):
        print(chunk)
```

Notice that this function utilizes the `pos_tag` function that tags each word with its part of speech. This clearly shows how one is building upon the other. Then we're using the `RegexParser` to pull out the tags we're interested in[^NLTK]. Let's start with **noun** combinations.

```python
# Chunk 1: Noun followed by Noun
reg_chunker(raw, r'NP: {<NN.?>+<NN.?>}')
```
```text
(NP IM/NNP bot/NN)
(NP Artificial/NNP Conversational/NNP Entity/NNP)
(NP computer/NN program/NN)
(NP Turing/NNP test/NN)
(NP dialog/NN systems/NNS)
(NP customer/NN service/NN)
(NP information/NN acquisition/NN)
(NP language/NN processing/NN systems/NNS)
(NP simpler/NN systems/NNS)
(NP wording/NN pattern/NN)
```

We can see interesting chunks identified such as **Artificial Conversational Entity**, **Turing test**, **customer service**, and **language processing systems**. These are more useful than the individual words. Let's look at **adjectives** paired with **nouns**.

```python
# Chunk 2: Adjective Follwed by Singular Noun
reg_chunker(raw, r'NP: {<JJ>+<NN>}')
```
```text
(NP interactive/JJ agent/NN)
(NP artificial/JJ intelligence/NN)
(NP conversational/JJ partner/NN)
(NP sophisticated/JJ natural/JJ language/NN)
(NP many/JJ simpler/NN)
(NP similar/JJ wording/NN)
```

Similar to the output above, we have **interactive agent**, **artificial intelligence**, **conversational partner**, and **sophisticated natural language** all showing us usage patterns. You can experiment with different regex patterns pulling out what you think is most useful.

## Noun Phrase Chunking with Spacy

Let's take a look at how **Spacy** handles chunking. Spacy is a modern and more sophisticated library for NLP and tends to have a simpler interface for many operations. Let's start with our imports and then explore how Spacy handles chunking.

```python
import spacy
nlp = spacy.load("en_core_web_sm")
```
Starting with a simple sentence from their docs, we can see how Spacy works.

```python
doc = nlp("Autonomous cars shift insurance liability toward manufacturers")
for chunk in doc.noun_chunks:
    print(chunk.text)
```
```text
Autonomous cars
insurance liability
manufacturers
```

Super easy, no fussing with `RegEx` and automatically pulling out different word combinations without needing to specify **POS tags**. Let's do the same with our paragraph.

```python
doc = nlp(raw)
for chunk in doc.noun_chunks:
    print(chunk.text)
```
```text
A chatbot
a talkbot
chatterbot
Bot
IM bot
interactive agent
Artificial Conversational Entity
a computer program
an artificial intelligence
which
a conversation
auditory or textual methods
Such programs
a human
a conversational partner
the Turing test
Chatbots
dialog systems
various practical purposes
customer service
information acquisition
Some chatterbots
sophisticated natural language processing systems
many simpler systems
keywords
the input
a reply
the most matching keywords
the most similar wording pattern
a database
```

You can see here that there is a high degree of overlap of the terms extracted via our two chunking patterns with NLTK. Spacy will also include the [determiner](https://en.wikipedia.org/wiki/Determiner) in the chunking process. We could also do this with NLTK, but our `RegEx` wasn't looking to extract it. One of the biggest differences you'll see is that Spacy automatically includes all different chunk combinations where a noun is the [head](https://en.wikipedia.org/wiki/Head_(linguistics)) word.


## Conclusion

From here, you can leverage Noun Chunks in your analysis to better identify what customers are talking about. In the post on POS tagging, I showed how you could separate products (nouns) from how people are talking about them. With Noun Phrase tagging, you can extract more specific product information for your analysis. I have a quick demo of this available; check out the full notebook on [Gitub](https://github.com/broepke/POS).


*If you liked what you read, [subscribe to my newsletter](https://campaign.dataknowsall.com/subscribe) and you will get my cheat sheet on Python, Machine Learning (ML), Natural Language Processing (NLP), SQL, and more. You will receive an email each time a new article is posted.*

## References

Photo by <a href="https://unsplash.com/@kylry?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Kyle Ryan</a> on <a href="https://unsplash.com/s/photos/phrases?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>

[^SPACY]: [Spacy: Industrial-Strength Natural Language Processing](https://spacy.io)
[^WIKI]: [Chatbot](https://en.wikipedia.org/wiki/Chatbot)
[^NLTK]: [Ch 7. Extracting Information from Text](https://www.nltk.org/book/ch07.html)

