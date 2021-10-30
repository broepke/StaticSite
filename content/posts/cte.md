Title: Common Table Expressions
Date: 2021-10-30
Modified: 2021-10-30
Category: SQL
Tags: datascience, sql
Slug: cte
Authors: Brian Roepke
Summary: Building complex select queries with CTEs.
Header_Cover: images/trees.jpg

## What is a Common Table Expression

When writing complex queries, it's often useful to break them up into smaller chunks both for readability and debugging.  Common Table Expressions or CTEs provide the ability to do this, and I've found them to be one of the most useful tools in my SQL toolbox.  

CTEs are very simple to implement.  They start with a simple `WITH` statement, the name of the new temporary table that you're going to `SELECT`.  They start like this:


```sql
WITH
    cte_name AS (
        SELECT
            ...
    )
```

The beauty is that you can chain multiple CTEs together.  As many as you'd like.  Let's take a look at what a couple of them would look like.

```sql
WITH
    cte_name AS (
        SELECT
            ...
    ),

another_cte AS (
    SELECT * FROM foo
    JOIN cte_name ON cte_name.id = foo.id
)

SELECT * FROM another_cte
LIMIT 10
```

That illustrates the concept well.  The first CTE creates a temporary table called `cte_name`, and the second CTE joins the `cte_name` table to the `foo` table in the second CTE.  You can use this pattern in multiple ways, but it simplifies constructing a complex query by breaking down logic into temporary tables is a very useful tool.

**Note:** One small thing to note is where the `,` is after the first CTE separates each temp table.  

Finally, you complete the process by running a standalone `SELECT` statement on the resulting temporary table.

Of course, in practice, the power is to run much more complex logic in each one.  Each CTE can contain any number of `SELECT` statements, `JOIN` statements, `WHERE` statements, etc.  Use them to structure your query for readability and understandability.

**Tip:** For easy debugging or even while building your query, you can test each of the CTEs by simply commenting out the rest of the code and running a select after each of them.  Like this. 

```sql
WITH
    cte_name AS (
        SELECT
            ...
    ) --, Make sure to comment out the comma

SELECT * FROM cte_name
LIMIT 10

-- another_cte AS (
--     SELECT * FROM foo
--     JOIN cte_name ON cte_name.id = foo.id
-- )

-- SELECT * FROM another_cte
-- LIMIT 10
```

## References

1. [Common Table Expressions: When and How to Use Them](https://chartio.com/resources/tutorials/using-common-table-expressions/)
2. [MySQL: WITH (Common Table Expressions)](https://dev.mysql.com/doc/refman/8.0/en/with.html)