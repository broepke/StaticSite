Title: Getting Started with Snowflake and the Rise of ELT Workflows in the Cloud
Date: 2022-09-22
Modified: 2022-09-22
Status: draft
Tags: bi, analytics, datascience, datawarehouse, snowflake
Slug: snowflakestart
Authors: Brian Roepke
Summary: How Modern Data Warehouses like Snowflake are changing the way we load and transform data right in our warehouse with no extra tooling needed.
Description: How Modern Data Warehouses like Snowflake are changing the way we load and transform data right in our warehouse with no extra tooling needed.
Header_Cover: images/covers/snowflake.jpg
Og_Image: images/covers/snowflake.jpg
Twitter_Image: images/covers/snowflake.jpg


# What is Snowflake?

Snowflake is a cloud-based data warehouse that is designed to be easy to use and fast. It is a fully managed service that is easy to get started with. Snowflake has gained temendous populariy due to its cloude native approach, speed, and ease of use.  Some of the world's largest companies use snowflake but it can also be used by any sized organization.

Some of the features of Snowflake are:

* **Separation of storage and compute**, which allows users to scale both resources dynamically and independently of each other.
* **Flexible pricing** model that allows users to pay for only the resources they use.
* Support for **multiple public cloud providers** like Amazon Web Services (AWS) or Microsoft Azure  and Google Cloud Platform (GCP) which lets you run snowflake in the same region as your other cloud services saving you on networking costs.
* The ability to **Time Travel** which allows you access to historical data where you can perform operations such as **undrop** a table that was accidentally deleted or even **undo a query** that updated data incorrectly.

In this post, I will show you how to get started with Snowflake and how to perfor Extract,  Load, and Transform (ELT) workflows.

## ELT versus ETL

Traditionally, the way data was loaded into a Data Warehouse was through a process called **Extract**, **Transform**, and **Load** or ETL.  In the ETL process, you would extract data from a source system and transfrom it with some sort of compute like Apache Spark, and *then* load it into the warehouse in its final format.  However, with the rise of modern Data Warehouses like Snowflake, we invert the second and third parts of the process to perform **Extract**, **Load**, and **Transform**.

**Stages** are used for both ELT and ETL, but with ELT, the staging area is in a database along side your normal tables, views, and more.  Take a look at the image below to see them directly along side each other.

![Snowflake Stages]({static}../../images/posts/snowflake_stages.png)

## Create a Snowflake Trial Account

To get, head over to their site and createa a [Snowflake 30-Day Trial](https://signup.snowflake.com/).   After registering you will need to choose a few basic things such as the the cloud provider of your choice as well as the region to run it in.  No credit card information is needed unless you choose to upgrade to a paid account.

![Snowflake Trial]({static}../../images/posts/snowflake_trial.png)

## Create a Warehouse

Next we need to create a **Warehouse**.  A warehouse in Snowflake nomenclature is not a place to store data, but rather the **compute resources**.  Snowflake allows you to create multiple warehouses, giving the ability to both track different types of jobs, as well as to adjust the scale up and down for different types of jobs.  For example, if you want to run a large ETL job, you can create a warehouse with a large number of cores and then scale it down when the job is complete.

![Snowflake Create a Warehouse]({static}../../images/posts/snowflake_warehouse_1.png)

Note that in the drop-down for the size, it allows you to go from **X-Small** which costs 1 credit per hour, up to the massive **6X-Large** which is a whopping 512 credits an hour!  It's important to note that Snowflake supports **auto-suspend** and **auto-resume**.  The warehouses will shut themselves down automatically when not in use to avoid running up a bill when you're not doing work.  

![Snowflake Create a Warehouse]({static}../../images/posts/snowflake_warehouse_2.png)


## Putting it Into Practice

```sql
create database weather;
use role sysadmin;
use warehouse elt;
use database weather;
use schema public;
```


```sql
-- Note the variant type for JSON data.  V is the column name
create table json_weather_data (v variant);
```

### Loading Data

Now we can create our **stage** and set the source for the loading.  A simple as this two lines of code to load your data into Snowflake.

```sql
-- Load the data from S3
create stage nyc_weather
url = 's3://snowflake-workshop-lab/zero-weather-nyc';
```

Next we can use the `list` command with the `@` symbol to list the files in the stage.  This is a great way to see what files are in the stage and to make sure that you are loading the correct files.

```sql
-- See what's in the stage
list @nyc_weather;
```

![JSON Files Loaded Into Stage]({static}../../images/posts/snowflake_files_staged.png)

```sql
copy into json_weather_data
from @nyc_weather 
    file_format = (type = json strip_outer_array = true);
    
select * from json_weather_data limit 10;
```

![Raw JSON]({static}../../images/posts/snowflake_json.png)

```text
{
  "coco": 7,
  "country": "US",
  "dwpt": 18.3,
  "elevation": 4,
  "icao": "KJFK",
  "latitude": 40.6333,
  "longitude": -73.7667,
  "name": "John F. Kennedy Airport",
  "obsTime": "2016-07-05T00:00:00.000Z",
  "prcp": 0,
  "pres": 1015.3,
  "region": "NY",
  "rhum": 76,
  "snow": null,
  "station": "74486",
  "temp": 22.8,
  "timezone": "America/New_York",
  "tsun": null,
  "wdir": 190,
  "weatherCondition": "Light Rain",
  "wmo": "74486",
  "wpgt": null,
  "wspd": 31.7
}
```

### Transforming Data

```sql
-- create a view that will put structure onto the semi-structured data
create or replace view json_weather_data_view as
select
    v:obsTime::timestamp as observation_time,
    v:station::string as station_id,
    v:name::string as city_name,
    v:country::string as country,
    v:latitude::float as city_lat,
    v:longitude::float as city_lon,
    v:weatherCondition::string as weather_conditions,
    v:coco::int as weather_conditions_code,
    v:temp::float as temp,
    v:prcp::float as rain,
    v:tsun::float as tsun,
    v:wdir::float as wind_dir,
    v:wspd::float as wind_speed,
    v:dwpt::float as dew_point,
    v:rhum::float as relative_humidity,
    v:pres::float as pressure
from
    json_weather_data
where
    station_id = '72502';
```

```sql
select * from json_weather_data_view
where date_trunc('month',observation_time) = '2018-01-01'
limit 10;
```

![Raw JSON]({static}../../images/posts/snowflake_final.png)


To see more on this workflow using data from MongoDB, check out my article [How to Normalize MongoDB Data in Snowflake for Data Science Workflows]({filename}normalizemongo.md) and to run through the whole Snowflake quick start tutorial visit [Snowflake Quickstarts](https://quickstarts.snowflake.com/guide/getting_started_with_snowflake/index.html#0)

## Conclusion




## References

Snowflake photo by <a href="https://unsplash.com/@aaronburden?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Aaron Burden</a> on <a href="https://unsplash.com/s/photos/snowflake?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
  
  
  
