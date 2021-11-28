Title: Text Cleaning for NLP in Python
Date: 2021-09-25
Modified: 2021-09-25
Tags: datascience, python, nlp, machine learning
Slug: textcleaning
Authors: Brian Roepke
Summary: A powerful function to clean text data.
Header_Cover: images/covers/botswana.jpg
Og_Image: images/covers/botswana.jpg
Twitter_Image: images/covers/botswana.jpg

## Cleaning Text

One of the most common tasks in Natural Language Processing (NLP) is to clean text data.  In order to maximize your results, it's important to distill you text to the most important root words in the corpus.  This post will show how I typically accomplish this.  The following are general steps in text preprocessing:

* **Tokenization**: Tokenization breaks the text into smaller units vs. large chunks of text. We understand these units as words or sentences, but a machine cannot until they’re separated. Special care has to be taken when breaking down terms so that logical units are created. Most software packages handle edge cases (U.S. broke into the US and not U and S), but it’s always essential to ensure it’s done correctly.
* **Cleaning**: The cleaning process is critical to removing text and characters that are not important to the analysis. Text such as URLs, noncritical items such as hyphens or special characters, web scraping, HTML, and CSS information are discarded.
* **Removing Stop Words**: Next is the process of removing stop words. Stop words are common words that appear but do not add any understanding. Words such as “a” and “the” are examples. These words also appear very frequently, become dominant in your analysis, and obscure the meaningful words.:
* **Spelling**: Spelling errors can also be corrected during the analysis. Depending on the medium of communication, there might be more or fewer errors. Official corporate or education documents most likely contain fewer errors, where social media posts or more informal communications like email can have more. Depending on the desired outcome, correcting spelling errors or not is a critical step.
* **Stemming and Lemmatization**: Stemming is the process of removing characters from the beginning or end of a word to reduce it to their stem. An example of stemming would be to reduce “runs” to “run” as the base word dropping the “s,” where “ran” would not be in the same stem. However, Lemmatization would classify “ran” in the same lemma.

The following is a script that I’ve been using to clean a majority of my text data.  

### Imports

```python
import pandas as pd
import re
import string
from bs4 import BeautifulSoup
import nltk
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import spacy
```

### Cleaning HTML

Removing HTML is optional and depending on what your data source is. I’ve found beautiful soup is the best way to clean this versus RegEx.

```python
def clean_html(html):
    
    # parse html content
    soup = BeautifulSoup(html, "html.parser")
  
    for data in soup(['style', 'script', 'code', 'a']):
        # Remove tags
        data.decompose()
  
    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)
```

### Cleaning the Rest

Now the workhorse.  

1. Make the text **lowercase**.  As you probably know, NLP is case-sensitive.
2. Remove **line breaks**.  Again, depending on your source, you might have encoded line breaks.
3. Remove **punctuation**.  This is using the string library.  Other punctuation can be added as needed.
4. Remove **stop words** using the NLTK library.  There is a list in the next line to add additional stop words to the function as needed.  These might be noisy domain words or anything else that makes the contextless clear.
5. Removing **numbers**.  Optional depending on your data.
6. **Stemming** or **Lemmatization**.  This process is an argument in the function.  You can choose either one via with `Stem` or `Lem`.  The default is to use none.


```python
# Load spacy
nlp = spacy.load('en_core_web_sm')

def clean_string(text, stem="None"):
    
    final_string = ""
    
    # Make lower
    text = text.lower()

    # Remove line breaks
    text = re.sub('\n', '', text)

    # Remove puncuation
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)

    # Remove stop words
    text = text.split()
    useless_words = nltk.corpus.stopwords.words("english")
    useless_words = useless_words + ['hi', 'im']
    
    text_filtered = [word for word in text if not word in useless_words]
    
    # Remove numbers
    text_filtered = [re.sub('\w*\d\w*', '', w) for w in text_filtered]
    
    # Stem or Lemmatize
    if stem == 'Stem':
        stemmer = PorterStemmer() 
        text_stemmed = [stemmer.stem(y) for y in text_filtered]
    elif stem == 'Lem':
        lem = WordNetLemmatizer()
        text_stemmed = [lem.lemmatize(y) for y in text_filtered]
    elif stem == 'Spacy':
        text_filtered = nlp(' '.join(text_filtered))
        text_stemmed = [y.lemma_ for y in text_filtered]
    else:
        text_stemmed = text_filtered
    
    final_string = ' '.join(text_stemmed)
    
    return final_string
```

### Example

To apply this to a standard data frame, use `apply` function from Pandas like below.  Let's take a look at the starting text:

```html
<p><a href="https://forge.autodesk.com/en/docs/data/v2/tutorials/download-file/#step-6-download-the-item" rel="nofollow noreferrer">https://forge.autodesk.com/en/docs/data/v2/tutorials/download-file/#step-6-download-the-item</a></p>\n\n<p>I have followed the tutorial and have successfully obtained the contents of the file, but where is the file being downloaded. In addition, how do I specify the location of where I want to download the file?</p>\n\n<p>Result on Postman\n<a href="https://i.stack.imgur.com/VrdqP.png" rel="nofollow noreferrer"><img src="https://i.stack.imgur.com/VrdqP.png" alt="enter image description here"></a></p>\n
```

Let's start by cleaning the HTML.

```python
# To remove HTML first and apply it directly to the source text column.
df['body'] = df['body'].apply(lambda x: clean_html(x))
```

After applying the function to clean HTML, this is the result:

```html
I have followed the tutorial and have successfully obtained the contents of the file, but where is the file being downloaded. In addition, how do I specify the location of where I want to download the file? Result on Postman
```

Next let's apply the `clean_string` function.

```python
# Next apply the clean_string function to the text
df['body_clean'] = df['body'].apply(lambda x: clean_string(x, stem='Stem'))
```

And the final resulting text:

```html
follow tutori success obtain content file file download addit specifi locat want download file result postman
```

Fully clean and ready to use in your NLP project.

**Note:** I often create a new column like above, `body_clean`, so I preserve the original in case punctuation is needed.

And that’s about it.  The order in the above function does matter.  You should complete certain steps before others, such as making lowercase first.  The function contains one RegEx example for removing numbers; a solid utility function that you can adjust to remove other items from the text using RegEx.

## Spacy vs. NLKT Lemmatization

The above function contains two different ways to Lemmatize your text.  The NLTK `WordNetLemmatizer` requires a Part of Speech (POS) argument (`noun`, `verb`) and therefore either requires multiple passes to get each word or will only capture one POS.  The alternative is to use `Spacy` which will automatically lemmatize each word and determine which POS it belongs to.  The issue is that Spacy's performance will be signficantly slower than NLTK.

## References

[^TXT]: [Text Processing Is Coming](https://towardsdatascience.com/text-processing-is-coming-c13a0e2ee15c)
[^LEM]: [Stemming vs Lemmatization](https://towardsdatascience.com/stemming-vs-lemmatization-2daddabcb221)