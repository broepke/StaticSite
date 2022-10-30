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



```python
import pandas as pd
import psycopg2
import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus
```


```python
import pandas as pd
import psycopg2
import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus
```



```python
user = os.environ.get("USER")
pw = os.environ.get("PASS")
db = os.environ.get("DB")
host = os.environ.get("HOST")
api = os.environ.get("API")
port = 5432
```



```python
uri = f"postgresql+psycopg2://{quote_plus(user)}:{quote_plus(pw)}@{host}:{port}/{db}"
alchemyEngine = create_engine(uri)
```

```python
q = """SELECT * FROM person_2b36d5aa_d186_408b_aa18_a6657382bf05 LIMIT 10"""
```

```python
dbConnection = alchemyEngine.connect();
```

```python
df = pd.read_sql(q, dbConnection);
```

```python
df.head()
```

```python
dbConnection.close();
```

## Conclusion



*If you liked what you read, [subscribe to my newsletter](https://campaign.dataknowsall.com/subscribe) and you will get my cheat sheet on Python, Machine Learning (ML), Natural Language Processing (NLP), SQL, and more. You will receive an email each time a new article is posted.*

## References

Baby Elephant Photo by <a href="https://unsplash.com/@eadesstudio?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">James Eades</a> on <a href="https://unsplash.com/s/photos/baby-elephant?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>