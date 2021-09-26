Title: Text Cleaning for NLP in Python
Date: 2021-09-25
Modified: 2021-09-25
Category: Python
Tags: aws, datascience, python, nlp
Slug: textcleaning
Authors: Brian Roepke
Summary: A powerful function to clean text data.
Header_Cover: images/botswana.jpg

## Cleaning Text

One of the most common tasks in Natural Language Processing (NLP) is to clean text data.  There are several steps that you should take to ensure that the various methods applied are maximized.  Here are a few common steps:

* **Tokenization**: Tokenization breaks the text into smaller units vs. large chunks of text. We understand these units as words or sentences, but a machine cannot until they’re separated. Special care has to be taken when breaking down terms so that logical units are created. Most software packages handle edge cases (U.S. broke into the US and not U and S), but it’s always essential to ensure it’s done correctly.
* **Cleaning**: The cleaning process is critical to removing text and characters that are not important to the analysis. Text such as URLs, noncritical items such as hyphens or special characters, web scraping, HTML, and CSS information are discarded.
* **Removing Stop Words**: Next is the process of removing stop words. Stop words are common words that appear but do not add any understanding. Words such as “a” and “the” are examples. These words also appear very frequently, become dominant in your analysis, and obscure the meaningful words.:
* **Spelling**: Spelling errors can also be corrected during the analysis. Depending on the medium of communication, there might be more or fewer errors. Official corporate or education documents most likely contain fewer errors, where social media posts or more informal communications like email can have more. Depending on the desired outcome, correcting spelling errors or not is a critical step. 
Lemmatization is the process of determining the lemma, or canonical form of a word.
* **Stemming and Lemmatization**: Stemming is the process of removing characters from the beginning or end of a word to reduce it to their stem. An example of stemming would be to reduce “runs” to “run” as the base word dropping the “s,” where “ran” would not be in the same stem. However, Lemmatization would classify “ran” in the same lemma.

The following is a script that I’ve been using to clean a majority of my text data.  

### Imports

```{python}
import re
import string
from bs4 import BeautifulSoup
import nltk
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
```

### Cleaning HTML

Removing HTML is optional and depending on what your data source is. I’ve found beautiful soup is the best way to clean this versus RegEx.

```{python}
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
6. Stemming or Lemmatization.  This process is an argument in the function.  You can choose either one via with `Stem` or `Lem`.  The default is to use none.   I typically use Lemmatization.


```{python}
def clean_string(text, stem="None"):
    
    final_string = ""
    
    # Make lower
    text = text.lower()

    # Remove line breaks
    text = re.sub('\n', '', text)

    # Remove puncuation
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)

    text = text.split()
    useless_words = nltk.corpus.stopwords.words("english")
    useless_words = useless_words + ['hi', 'im']
    
    # Remove stop words
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
    else:
        text_stemmed = text_filtered
    
    for word in text_stemmed:
        final_string += word + " "
    
    return final_string
```

To apply this to a standard data frame, use the `apply` method like so:

```{python}
# To remove HTML first and apply it directly to the source text column.
df['body'] = df['body'].apply(lambda x: clean_html(x))

# Next apply the clean_string function to the text
df['body_clean'] = df['body'].apply(lambda x: clean_string(x, stem='Lem'))
```

**Note:** I often create a new column like above, `body_clean`, so I preserve the original in case punctuation is needed.

And that’s about it.  The order in the above function does matter.  You should complete certain steps before others, such as making lowercase first.  The function contains one RegEx example for removing numbers; a solid utility function that you can adjust to remove other items from the text using RegEx. You can read about it a little here: 

[Text Processing Is Coming](https://towardsdatascience.com/text-processing-is-coming-c13a0e2ee15c)