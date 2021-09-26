Title: Text Cleaning for NLP in Python
Date: 2021-09-25
Modified: 2021-09-25
Category: Python
Tags: aws, datascience, python, nlp
Slug: textcleaning
Authors: Brian Roepke
Summary: A powerful function to clean text data.
Header_Cover: images/cranes_day.jpg

## Cleaning Text

One of the most common tasks in Natural Language Processing (NLP) is to clean text data.  There are several steps that you should take in order to ensure that the various methods applied are maximized.  Here are a few common steps:

* **Tokenization**: Tokenization breaks the text into smaller units vs. large chunks of text. We understand these units as words or sentences, but a machine cannot until they’re separated. Special care has to be taken when breaking down terms so that logical units are created. Most software packages handle edge cases (U.S. broke into the US and not U and S), but it’s always essential to ensure it’s done correctly.
* **Cleaning**: The cleaning process is the critical step of removing text and characters that are not important to the analysis. Text such as URLs, noncritical items such as hyphens or special characters, web scraping, HTML, and CSS information are discarded.
Removing Stop Words: Next is the process of removing stop words. Stop words are common words that appear but not to add any understanding. Words such as “a” and “the” are examples. These words also appear very frequently, become dominant in your analysis, and obscure the meaningful words.:
* **Spelling**: Spelling errors can also be corrected during the analysis. Depending on the medium of communication, there might be more or fewer errors. Official corporate or education documents most likely contain fewer errors, where social media posts or more informal communications like email can have more. Depending on the desired outcome, correcting spelling errors or not is a critical step. 
* **Stemming and Lemmatization**: Stemming is the process of removing characters from the beginning or end of a word to reduce it to their stem. Lemmatization is the process of determining the lemma, or canonical form of a word (Berger et al., 2020). An example of stemming would be to reduce “runs” to “run” as the base word dropping the “s,” where “ran” would not be in the same stem. However, Lemmatization would classify “ran” in the same lemma.

The following is a script that i've been using to clean a majority of my text data.  

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

To apply this to a standard dataframe, simply use the `apply` method like so:

```{python}
df['title_clean'] = df['title'].apply(lambda x: clean_string(x, stem='Lem'))
```

Note: I often create a new column like above, `title_clean` so I preseve the original in case the context of punctuation is needed.