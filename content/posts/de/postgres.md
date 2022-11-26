Title: A Quick Start to Connecting to PostgreSQL and Pulling Data into Pandas
Date: 2022-11-11
Modified: 2022-11-11
Status: draft
Tags: analytics, datascience, databases, sql
Slug: postgres
Authors: Brian Roepke
Summary: Get you on your way to data analysis and model building quickly by pulling PostgreSQL data into Pandas.
Description: As a data scientist, you want your data in a data frame; here's how you can quickly pull PostgreSQL tables into Pandas so you can start building models.
Header_Cover: images/covers/elephant.jpg
Og_Image: images/covers/elephant.jpg
Twitter_Image: images/covers/elephant.jpg

# A Quick Start to Connecting to PostgreSQL and Pulling Data into Pandas

PostgreSQL is a powerful relational database management system (RDBMS) that is used by many companies and organizations. Connecting to it is easy, and thanks to the awesome Python ecosystem, getting your data into a Data Frame in Pandas is just as easy.  Let's take a look at a simple example that will help you get started.

## Imports

The first thing we'll do is to import the libraries we will need.  We will need the `psycopg2` library to connect to PostgreSQL, and the `pandas` library to work with our data. in addition we're going to use `pandas`, `os`, `urllib`, and `sqlalchemy` to help us connect to our database. 


```python
import pandas as pd
import psycopg2
import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus
```

Next we want to make sure we're not hard coding our sensitive information but rather pulling them from environment variables.  If you'd like to learn more about this process, check out the this [article]({filename}../other/envvar.md).

```python
user = os.environ.get("USER")
pw = os.environ.get("PASS")
db = os.environ.get("DB")
host = os.environ.get("HOST")
api = os.environ.get("API")
port = 5432
```

Next, we need to ensure any information in our connection string is **properly encoded** like the username and password which can be easily achieved with the `quote_plus` function from `urllib`. Let's take a quick look at a sample password and how it is encoded.

```python
fake_pw = "p@ssw0rd'9'!"
print(quote_plus(fake_pw))
```
```text
p%40ssw0rd%279%27%21
```

Next, we can create our **connection string**.  This is a string that contains all the information needed to connect to our database.  We will use string format (`f` in front of the string) to insert our variables into the string.  We will also use the `quote_plus` function to encode our username and password.

In addition to the connection string, we will also create a **SQLAlchemy engine**. 

```python
uri = f"postgresql+psycopg2://{quote_plus(user)}:{quote_plus(pw)}@{host}:{port}/{db}"
alchemyEngine = create_engine(uri)
```

That's it! Assuming you didn't receive an error, you are now connected to your PostgreSQL database.  Let's take a look at how we can pull data into a Pandas Data Frame.  

First we'll define a query in the form of a string.  A best practice here is to use triple quotes (`"""`).  This allows us to write our query over multiple lines as well as avoid conflicts when our query itself contains quotes, such as `WHERE name = 'Brian'`.

```python
q = """SELECT * FROM person LIMIT 10"""
```

Next, we will create the connection itself off of the `alchemyEngine` we created earlier.

```python
dbConnection = alchemyEngine.connect();
```

We will then use the `read_sql` function from `pandas` to pull our data into a Data Frame.

```python
df = pd.read_sql(q, dbConnection);
```

Now that we have a dataframe and can display the 

```python
df.head()
```

A best practice is to close your connection when you're done.  

```python
dbConnection.close();
```

## Conclusion

PostgreSQL is a powerful relational database management system (RDBMS) that is used by many companies and organizations. We covered connecting to it and getting your data into a Pandas Dataframe.  We also discussed some best practices like storing credentials in Environment Variables and how to easily URL encode your username and password, which often will have characters that are not supported.

*If you liked what you read, [subscribe to my newsletter](https://campaign.dataknowsall.com/subscribe) and you will get my cheat sheet on Python, Machine Learning (ML), Natural Language Processing (NLP), SQL, and more. You will receive an email each time a new article is posted.*

## References

Photo by <a href="https://unsplash.com/@sergiferrete?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Sergi Ferrete</a> on <a href="https://unsplash.com/s/photos/elephant?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
  