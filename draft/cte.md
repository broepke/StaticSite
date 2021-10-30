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

CTEs are very simple to implement.  They start with a simple `WITH` statement, the name of the new temoporary table that you're going to `SELECT`.  They start like this:


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
    SELECT * from foo
    join cte_name on cte_name.id = foo.id
)

select * from another_cte
```

That illustrates the concept well.  The first CTE creates a temporary table called `cte_name` and the second CTE joins the `cte_name` table to the `foo` table in the second CTE.  This pattern can be used in multiple ways, but the fact that it simplifies constructing a complex query by breaking down logic into temporary tables is a very useful tool.

**Note:** One small thing to note is where the `,` is after the first CTE.  That separates each of the temp tables.  Finally, you complete the process by running a standalone `SELECT` statement on the resulting temporary table.



## References

1. [Common Table Expressions: When and How to Use Them](https://chartio.com/resources/tutorials/using-common-table-expressions/)
2. 
