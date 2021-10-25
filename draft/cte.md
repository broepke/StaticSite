Title: Common Table Expressions
Date: 2021-10-24
Modified: 2021-10-24
Category: SQL
Tags: datascience, sql
Slug: cte
Authors: Brian Roepke
Summary: Building complex select queries with CTEs.
Header_Cover: images/trees.jpg

## What is a Common Table Expression

When writing complex queries it's often useful to break them up into smaller chunks both for readability as well as for debugging.  Common Table Expressions, or CTEs provide the ability to do this and I've found them to be one of the most useful tools in my SQL tool box.  

CTEs are very simple to implement.  They start with a simple `WITH` statement, the name of the new temoporary table that you're going to `SELECT` 


```sql
WITH
    cte_name AS (
        SELECT
            ...
    )
```

## References

1. [Common Table Expressions: When and How to Use Them](https://chartio.com/resources/tutorials/using-common-table-expressions/)
2. 
