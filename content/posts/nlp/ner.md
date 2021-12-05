Title: Named Entity Recognition
Date: 2021-12-04
Modified: 2021-12-04
Status: draft
Tags: datascience, nlp
Slug: ner
Authors: Brian Roepke
Summary: Classify text into pre-defined categories such as person names, organizations, locations, and more!
Header_Cover: images/covers/dc.jpg
Og_Image: images/covers/dc.jpg
Twitter_Image: images/covers/dc.jpg
## What is Named Entity Recognition?


```python
import spacy
from spacy import displacy

text = "Mr. Biden’s announcement came as several new cases of the Omicron variant were reported in the United States, including five people in New York State, a Minnesota resident who had recently traveled to New York City and a Colorado resident who had recently returned from southern Africa. Hawaii also reported its first known case, and California its second."

nlp = spacy.load("en_core_web_sm")
doc = nlp(text)
displacy.render(doc, style="ent")
```
## References

Photo by <a href="https://unsplash.com/@connave?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Bob Bowie</a> on <a href="https://unsplash.com/s/photos/washington-dc?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>

[^SPACY]: [Spacy: Industrial-Strength Natural Language Processing](https://spacy.io)

```text
file:///Users/brianroepke/Projects/DATA110/Week%208/DATA110_Week8-broepke.html
file:///Users/brianroepke/Projects/DATA110/Week%2011/DATA110-Week11-Midterm-broepke.html 
```