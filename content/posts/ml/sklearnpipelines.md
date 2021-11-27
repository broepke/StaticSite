Title: Using Pipelines in Sci-kit Learn
Date: 2021-10-01
Modified: 2021-10-01
Tags: datascience, python, machine learning
Slug: sklearnpipelines
Authors: Brian Roepke
Summary: Why you should be using pipelines and not processing steps separately.
Header_Cover: images/cranes_night.jpg
Og_Image: images/cranes_night.jpg
Twitter_Image: images/cranes_night.jpg

## Why Pipelines?

When I started building models in Sklearn, I would break each pre-processing step into its cell or chunk of code.  This was a good way to get started because you could easily break down the steps into readable chunks.  However, while it was easier to read, it ended up lacking repeatability.  The next time you presented your model with new data, you had to run through all the steps to transform the data before running the model on the new data, which presented many problems.  For example the dimensionality of your data can change if there are new columns created during One Hot Encoding.

The Answer? [Pipelines](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html#sklearn.pipeline.Pipeline)

## Anatomy of a Pipeline

First, as usual, the imports needed to run this script.

```Python
from sklearn.pipeline import Pipeline
from sklearn.compose import make_column_selector as selector
from sklearn.compose import ColumnTransformer
from sklearn. pre-processing import MinMaxScaler
from sklearn. pre-processing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
```

### Column Tranformers

Next is a function for making a column transformer.  I prefer to call this as a function to make the code more reusable.

The column transformer allows you to combine any number of pre-processing steps into a single transformer.  In the example below, we have a `MinMaxScaler` for numeric columns and an `OneHotEncoder` for categorical values.  You could include any transformer from Sklearn in these steps.

A good example of this from their documentation:  
[Column Transformer with Mixed Types](https://scikit-learn.org/stable/auto_examples/compose/plot_column_transformer_mixed_types.html#sphx-glr-auto-examples-compose-plot-column-transformer-mixed-types-py)

In addition to demonstrating both numeric and categorical columns, this shows the [column selector](https://scikit-learn.org/stable/modules/generated/sklearn.compose.make_column_selector.html) which allows you to select groups of columns based on different criteria.  The numeric columns are selected via `selector(dtype_exclude="object")`.  Below demonstrates selecting columns by their name as a simple python list.  You can combine any of these select styles with each of the different transformers you supply.  Additionally, you name your transformers such as `num` and `cat` as see below for later identification in your fit model. 


```python
def make_coltrans():
    column_trans = ColumnTransformer(transformers=
            [('num', MinMaxScaler(), selector(dtype_exclude="object")),
             ('cat', OneHotEncoder(dtype='int', handle_unknown='ignore'), ['CAT_FIELD_ONE', 'CAT_FIELD_TWO'])],
            remainder='drop')
    
    return column_trans
```

### The Pipeline

The creation of the pipeline now is a very simple step after creating the column transformer.  All you need to do is order the pipeline sequence based on the logical ordering of the steps you would normally take.  Here we have two steps, the column transformer, and the classifier.  Like the column transformer, we name the steps like `prep` and `clf` below.

```python
def create_pipe(clf):
    '''Create a pipeline for a given classifier.  The classifier needs to be an instance
    of the classifier with all parmeters needed specified.'''
    
    # Each pipeline uses the same column transformer.  
    column_trans = make_coltrans()
    
    pipeline = Pipeline([('prep',column_trans),
                         ('clf', clf)])
     
    return pipeline
```

### Creating and Fitting the Model

Finally, we can create an instance of the classifier and pass that to our function above that create the pipeline.

```python
# Creaate the classifier instance and build the pipleline.
clf = RandomForestClassifier(random_state=42, class_weight='balanced')
pipeline = create_pipe(clf)

# Fit the model to the training data
pipeline.fit(X_train, y_train)

```

## Summary

The above demonstrates the simplicity of setting up a pipeline.  The first time you walk through this, it can seem a little confusing versus doing each step independently.  The benefit is that each time you want to apply this to a new model, or even better, run new data against your fit model, all of the transformation to the data will happen automatically. 