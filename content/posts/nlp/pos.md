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

Part of Speech (POS) is a way to describe the grammatical function of a word.  There are eight different parts of speech in English that are commonly defined [^POS].

1. **Noun**: A noun is the name of a person, place, thing, or idea.
2. **Pronoun**: A pronoun is a word used in place of a noun.
3. **Verb**: A verb expresses action or being.
4. **Adjective**: An adjective modifies or describes a noun or pronoun.
5. **Adverb**: An adverb modifies or describes a verb, an adjective, or another adverb.
6. **Preposition**: A preposition is a word placed before a noun or pronoun to form a phrase modifying another word in the sentence.
7. **Conjunction**: A conjunction joins words, phrases, or clauses.
8. **Interjection**: An interjection is a word used to express emotion. 



https://www.quora.com/What-are-the-applications-of-tagging-in-NLP 

There is a hierarchy of tasks in NLP (see Natural language processing for a list). At the bottom is sentence and word segmentation. POS tagging builds on top of that, and phrase chunking builds on top of POS tags. These tags in turn can be used as features for higher level tasks such as building parse trees, which can in turn be used for Named Entity Resolution, Coreference Resolution, Sentiment Analysis and Question Answering.


## References

Photo by <a href="https://unsplash.com/@apellaes?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Alexandre Pellaes</a> on <a href="https://unsplash.com/s/photos/conferences?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>

[^POS]: [The Eight Parts of Speech](https://www.butte.edu/departments/cas/tipsheets/grammar/parts_of_speech.html)
[^WIKI]: [Part of Speech on Wikipedia](https://en.wikipedia.org/wiki/Part_of_speech)
[^NLTK]: [NLTK: Natural Language Toolkit](https://www.nltk.org)
[^SPACY]: [Spacy: Industrial-Strength Natural Language Processing](https://spacy.io)
[^BLOB]: [TextBlob: Simplified Text Processing](https://textblob.readthedocs.io/en/dev/)