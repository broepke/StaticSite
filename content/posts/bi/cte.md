Title: 1 Trick That Changed the Way I Write Queries Forever
Date: 2021-10-24
Modified: 2021-10-24
Tags: datascience, sql, databases
Slug: cte
Authors: Brian Roepke
Summary: Leverage Common Table Expressions to Simplify the Writing and Troubleshooting Complex Queries
Header_Cover: images/covers/cabinet.jpg

## What is a Common Table Expression

When writing complex queries, it's often useful to break them up into smaller chunks both for readability and debugging.  Common Table Expressions or CTEs provide the ability to do this, and I've found them to be one of the most useful tools in my SQL toolbox.  

CTEs are very simple to implement.  They start with a simple `WITH` statement, the name of the new CTE that you're going to `SELECT`.  They start like this:


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

That illustrates the concept well. The first CTE runs the first query and stores it in memory called `cte_name`, and the second CTE joins the `cte_name` table to the `foo` table in the second CTE.  You can use this pattern in multiple ways, but it simplifies constructing a complex query by breaking it down into logical parts.

**Note:** One small thing to note is where the `,` is after the first CTE separates each table.  

Finally, you complete the process by running a standalone `SELECT` statement on the resulting CTE.

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

## Example in Real Life
I wrote a query for a view I was creating in Snowflake. Without CTEs, this would have proven to be much more difficult.

```sql
WITH DAILY as (
    SELECT ID
    FROM "LOGS_DAILY"),

MAP AS (
    SELECT SOURCE_ID AS ID, ANY_VALUE(UUID) AS UUID
    FROM "CONTACT_MAP"
    WHERE SOURCE_ID_NAME = 'ID'
    AND DT = (SELECT MAX(DT) FROM "CONTACT_MAP")
    GROUP BY SOURCE_ID),
CONTACT AS (
    SELECT CONTACT_UUID, SITE_UUID
    FROM "CONTACT_MASTER"
    WHERE DT = (SELECT MAX(DT) FROM "CONTACT_MASTER")),


ACCOUNT AS (
    SELECT *
    FROM "ACCOUNT"
    WHERE SITE_STATUS = 'Active')

SELECT DISTINCT *
FROM DAILY
LEFT JOIN MAP ON MAP.ID = DAILY.ID
LEFT JOIN CONTACT ON CONTACT.CONTACT_UUID = MAP.CONTACT_UUID
LEFT JOIN ACCOUNT ON ACCOUNT.SITE_UUID = CONTACT.SITE_UUID
LIMIT 100
```

## Conclusion

Common Table Expressions or CTEs are a powerful tool in your Querying toolbox that allows you to take complex, layered SELECT statements, break them down into more manageable chunks, and then pull them back together in the end. If you’re not using them today, give them a try, and I’m confident they will be a regular

*If you liked what you read, [subscribe to my newsletter](https://campaign.dataknowsall.com/subscribe) and you will get my cheat sheet on Python, Machine Learning (ML), Natural Language Processing (NLP), SQL, and more. You will receive an email each time a new article is posted.*

## References

Photo by <a href="https://unsplash.com/@jankolar?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Jan Antonin Kolar</a> on <a href="https://unsplash.com/@jankolar?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
  

1. [Common Table Expressions: When and How to Use Them](https://chartio.com/resources/tutorials/using-common-table-expressions/)
2. [MySQL: WITH (Common Table Expressions)](https://dev.mysql.com/doc/refman/8.0/en/with.html)