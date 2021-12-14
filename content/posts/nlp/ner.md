Title: Named Entity Recognition
Date: 2021-12-19
Modified: 2021-12-19
Status: draft
Tags: datascience, nlp
Slug: ner
Authors: Brian Roepke
Summary: Classify text into pre-defined categories such as person names, organizations, locations, and more!
Header_Cover: images/covers/dc.jpg
Og_Image: images/covers/dc.jpg
Twitter_Image: images/covers/dc.jpg
## What is Named Entity Recognition?

[Named Entity Recognition](https://en.wikipedia.org/wiki/Named-entity_recognition) or NER is a technique for identifying and classifying named entities in text.  These entities are a level above [Part of Speech Tagging]({filename}pos.md) and [Noun Phrase Chunking]({filename}nounphrase.md) where instead of identifying gramical parts, it's actually identifying and classifying words as their proper entities.  The main categories that are recognized (before retraining) are:

```text
PERSON:      People, including fictional.
NORP:        Nationalities or religious or political groups.
FAC:         Buildings, airports, highways, bridges, etc.
ORG:         Companies, agencies, institutions, etc.
GPE:         Countries, cities, states.
LOC:         Non-GPE locations, mountain ranges, bodies of water.
PRODUCT:     Objects, vehicles, foods, etc. (Not services.)
EVENT:       Named hurricanes, battles, wars, sports events, etc.
WORK_OF_ART: Titles of books, songs, etc.
LAW:         Named documents made into laws.
LANGUAGE:    Any named language.
DATE:        Absolute or relative dates or periods.
TIME:        Times smaller than a day.
PERCENT:     Percentage, including ”%“.
MONEY:       Monetary values, including unit.
QUANTITY:    Measurements, as of weight or distance.
ORDINAL:     “first”, “second”, etc.
CARDINAL:    Numerals that do not fall under another type.
```

There are many libraries to choose from, my tool of choice these days is [SpaCy](https://spacy.io/).  It's powerful API and models are ready to go with a few lines of code, and as we'll see later, we can use it to train our own models.  To really demonstrate the power, let's take a look at it in action. 

## NER with Spacy

We'll start with a pargrah taken from a Teslarati article: [Tesla could receive $12.36 million worth of Model 3 orders from New York City](https://www.teslarati.com/tesla-new-york-city-12-million-model-3-order/).  



```python
import spacy
from spacy import displacy
nlp = spacy.load("en_core_web_sm")

text = "IN THE MATTER OF a proposed contract between the Department of Citywide Administrative Services of the City of New York and Tesla, Inc., located at 3500 Deer Creek Rd., Palo Alto, CA 94304, for procuring Tesla Model 3 All-Electric Sedans. The contract is in the amount of $12,360,000.00. The term of the contract shall be five years from date of Notice of Award. The proposed contractor has been selected by Sole Source Procurement Method, pursuant to Section 3-05 of the Procurement Policy Board Rules. If the plan does go through, the $12.36 million could effectively purchase about 274 units of the base Model 3 Rear-Wheel-Drive, which cost $44,990 under Tesla's current pricing structure."

doc = nlp(text)
displacy.render(doc, style="ent")
```

Spacy has a wonderful ability to render NER tags inline with the text.  This is a fantastic way to see what's being recognized in context of the orginal article.

<figure style="margin-bottom: 6rem"><div class="entities" style="line-height: 2.5; direction: ltr">IN THE MATTER OF a proposed contract between <mark class="entity" style="background: #7aecec; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">the Department of Citywide Administrative Services<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">ORG</span></mark> of the City of <mark class="entity" style="background: #feca74; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">New York<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">GPE</span></mark> and <mark class="entity" style="background: #7aecec; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">Tesla, Inc.<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">ORG</span></mark>, located at <mark class="entity" style="background: #e4e7d2; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">3500<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">CARDINAL</span></mark> Deer Creek Rd., <mark class="entity" style="background: #feca74; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">Palo Alto<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">GPE</span></mark>, CA 94304, for procuring Tesla Model 3 All-Electric Sedans. The contract is in the amount of $<mark class="entity" style="background: #e4e7d2; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">12,360,000.00<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">MONEY</span></mark>. The term of the contract shall be <mark class="entity" style="background: #bfe1d9; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">five years from date<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">DATE</span></mark> of Notice of Award. The proposed contractor has been selected by <mark class="entity" style="background: #7aecec; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">Sole Source Procurement Method<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">ORG</span></mark>, pursuant to <mark class="entity" style="background: #ff8197; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">Section 3-05<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">LAW</span></mark> of <mark class="entity" style="background: #7aecec; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">the Procurement Policy Board Rules<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">ORG</span></mark>. If the plan does go through, the <mark class="entity" style="background: #e4e7d2; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">$12.36 million<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">MONEY</span></mark> could effectively purchase <mark class="entity" style="background: #e4e7d2; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">about 274<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">CARDINAL</span></mark> units of the base Model 3 Rear-Wheel-Drive, which cost $<mark class="entity" style="background: #e4e7d2; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">44,990<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">MONEY</span></mark> under <mark class="entity" style="background: #7aecec; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">Tesla<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">ORG</span></mark>'s current pricing structure.</div></figure>


## Training Custom Entities

https://stackoverflow.com/questions/66779014/use-the-revit-native-file-language-instead-of-english-when-converting-properties 


```python
def built_spacy_ner(text, target, type):
    start = str.find(text, target)
    end = start + len(target)
    
    return (text, {"entities": [(start, end, type)]})
```

With the above function, we can pass in `text`, `target`, and `type` to get the correctly formatted tuple. The result is a list.

**Note:** One thing that I've seen (and read[^CAT]) in pactice, is that if you provide too many examples of text, it will overfit and end up not recognizing anything except your trained examples.  I started with trying to train the entire `DataFrame`, but it returned poor results.

```python
TRAIN_DATA = []
TRAIN_DATA.append(built_spacy_ner("I work for Autodesk.", "Autodesk", "ORG"))
```
The final format is a `tuple` with the original `string` and a `dictionary` with the entity `start` and `end` location in the `string` and its `type`.

```python
[('Model Derivative API provides translation', 
  {'entities': [(0, 20, 'API')]}),
 ('I want to create a cloud-based service connected to Revit Server.',
  {'entities': [(61, 73, 'PRODUCT')]}),
 ("I'm new to the Forge API unsure where a design parameter is required",
  {'entities': [(15, 24, 'API')]}),
 ('I would like to automate Revit with the Design Automation API',
  {'entities': [(40, 61, 'API')]}),
 ("I've uploaded a Revit model to my OSS bucket.",
  {'entities': [(34, 37, 'SERVICE')]}),
 ('Autodesk Forge is my Platform of choice',
  {'entities': [(0, 14, 'PRODUCT')]}),
 ('The native file format for Revit is RVT.',
  {'entities': [(36, 39, 'FORMAT')]}),
 ('I work for Autodesk.', {'entities': [(11, 19, 'ORG')]}),
 ('The Model Derivative API used in conjunction with the Viewer',
  {'entities': [(4, 24, 'API')]}),
 ('Changes are sent to a central BIM 360 server.',
  {'entities': [(30, 37, 'PRODUCT')]}),
 ('All of this is possible on IFC.', 
  {'entities': [(27, 30, 'FORMAT')]})]
```


### Before

<figure style="margin-bottom: 6rem"><div class="entities" style="line-height: 2.5; direction: ltr">I've been using for a long time the Model Derivative API from <mark class="entity" style="background: #aa9cfc; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">Autodesk Forge<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">PERSON</span></mark> to (successfully) export <mark class="entity" style="background: #feca74; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">Revit<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">GPE</span></mark> files to IFC. However, I notice that even when the original <mark class="entity" style="background: #feca74; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">Revit<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">GPE</span></mark> files are saved with the <mark class="entity" style="background: #c887fb; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">French<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">NORP</span></mark> version of the software (namely, <mark class="entity" style="background: #aa9cfc; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">Revit FRA<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">PERSON</span></mark>), the properties (e.g. ) are exported in <mark class="entity" style="background: #ff8197; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">English<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">LANGUAGE</span></mark> ( ), and I see no option in the Model Derivative API to force using the native language. Does someone have an idea on how to do that (if it is feasible)? I have searched on the official documentation and tried modifying the parameters mentioned for the conversion (see ), but with no success so far. Of course the same issue can be of interest for those exporting to other formats than IFC, or other languages than <mark class="entity" style="background: #c887fb; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">French<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">NORP</span></mark>. Thanks!</div></figure>






### After

<figure style="margin-bottom: 6rem"><div class="entities" style="line-height: 2.5; direction: ltr">I've been using for a long time the <mark class="entity" style="background: #ddd; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">Model Derivative API<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">API</span></mark> from <mark class="entity" style="background: #bfeeb7; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">Autodesk Forge<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">PRODUCT</span></mark> to (successfully) export Revit files to <mark class="entity" style="background: #ddd; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">IFC<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">FORMAT</span></mark>. However, I notice that even when the original Revit files are saved with the <mark class="entity" style="background: #c887fb; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">French<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">NORP</span></mark> version of the software (namely, <mark class="entity" style="background: #bfeeb7; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">Revit FRA<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">PRODUCT</span></mark>), the properties (e.g. ) are exported in English ( ), and I see no option in the <mark class="entity" style="background: #ddd; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">Model Derivative API<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">API</span></mark> to force using the native language. Does someone have an idea on how to do that (if it is feasible)? I have searched on the official documentation and tried modifying the parameters mentioned for the conversion (see ), but with no success so far. Of course the same issue can be of interest for those exporting to other formats than IFC, or other languages than <mark class="entity" style="background: #c887fb; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">French<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">NORP</span></mark>. Thanks!</div></figure>

## References

Photo by <a href="https://unsplash.com/@connave?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Bob Bowie</a> on <a href="https://unsplash.com/s/photos/washington-dc?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>

[^SPACY]: [Spacy: Industrial-Strength Natural Language Processing](https://spacy.io)
[^TDS]: [Named Entity Recognition: Applications and Use Cases](https://towardsdatascience.com/named-entity-recognition-applications-and-use-cases-acdbf57d595e)
[^MLPLUS]: [How to Train spaCy to Autodetect New Entities (NER) [Complete Guide]](https://www.machinelearningplus.com/nlp/training-custom-ner-model-in-spacy/)
[^CAT]: [Pseudo-rehearsal: A simple solution to catastrophic forgetting for NLP](https://explosion.ai/blog/pseudo-rehearsal-catastrophic-forgetting)