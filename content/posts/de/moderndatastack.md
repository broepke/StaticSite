Title: My Personal Modern Data Stack: How to Keep Current and Affordable
Date: 2023-03-21
Modified: 2023-03-21
Status: draft
Tags: analytics, datascience, databases, sql, dataengineering
Slug: moderndatastack
Authors: Brian Roepke
Summary: XXX
Description: XXX
Header_Cover: images/covers/containers.jpg
Og_Image: images/covers/containers.jpg
Twitter_Image: images/covers/containers.jpg

# What is My Modern Data Stack?

There is a term floating around called the **Modern Data Stack**.  It's a bit overused, but what it means is that you're taking advantage of the **best technology** out there.  The challenge with the modern data stack is that as an individual, you might struggle to get everyhing up and running for a very **low cost**.  For me, I want to learn, but i'm not going to drop *$10,000* in getting started fees for a workflow orchestration tool. I want to build a stack that helps me learn, stay relevant, and get the job done. Here is my current set of tools of choice! 

A note to vendors out there.  If your entry point is $10,000, or $30,000 or more, **You're doing SaaS wrong**.  Fix it.  I've sold enterprise software for decades and this price point means two things.  You don't have your operational expenses under control or you've purposesly decided to go after *only* enterprises to compensate for a poor GTM strategy.  

My criteria for selecting them is as follows.

* **Best In Class**: They should be the leader in their space, if possible, or offer a very similar experience to the leader.
* **Low Cost or Free**: Specifically for Small Teams and Individuals.  This includes ensuring that the free tier is usable in a basic workflow.
* **Great Documentation**: Great products have great documentation.  Each one of my selections are fantastic.
* **Ecosystem**: You want to ensure that you're not the only user. Are people asking questions in public forums? Are there accessible support channel if needed? 

## The Stack

![Modern Data Stack]({static}../../images/posts/moderndatastack_logos.png)

## Data Warehouse / Data Platform

The foundation of any data stack is a data warehouse or data platform.  Without a doubt, the best choice here is Snowflake.  You can sign up for a [30-Day Trial](https://signup.snowflake.com/) and then after that, just enter your credit card information.  As long as you're not processing a ton of data, the charges should be pretty minimal.  I've not found a *free* data warehouse, but since Snowflake is consumption based, you only pay for what you use.  

Snowflake is 100% cloud Native which makes it easy to connect the rest of your stack.  It also is the market leader and everything you learn here, should be portable to many professional situations.

Some of the key features of Snowflake are:

* **Separation of storage and compute** allows users to scale both resources dynamically and independently of each other.
* **Flexible pricing** model that allows users to pay for only the resources they use.
* Support for **multiple public cloud providers** like Amazon Web Services (AWS) or Microsoft Azure and Google Cloud Platform (GCP), which lets you run Snowflake in the same region as your other cloud services, saving you on networking costs.
* The ability to **Time Travel** allows you access to historical data where you can perform operations such as **undrop** a table that you accidentally deleted or even **undo a query** that updated data incorrectly.
* A unique **Data Sharing** feature allows you to share data with other users or organizations.
* A **Marketplace** full of data from third-party providers that you can use to enrich your warehouse.

**Cost:** Consumption based with 30-day free trial

**URL**: [https://signup.snowflake.com/](https://signup.snowflake.com/)

## Connector Sync Framework

Next up is a **connector based framework** that simplifies data engineering tasks.  If you can get the ability to sync your data off the shelf, then do it; don't write this yourself! Starting in 2023, Fivetran [annouced](https://fivetran.com/docs/getting-started/consumption-based-pricing/2023-cbp-faq) a Free tier of their product.

* You get **500,000 MAR** or "Monthly Active Records"
* **Unlimited** users
* **300+** fully-managed connectors
* **Automatic** schema migrations
* Integration for **dbt Core**
* **15-min** syncs
* Access to Fivetran’s **REST API**

There is nothing easier, or better than this product for **most**, if not all, of your data sync jobs.  If you're working in an enterprise, you will probably encounter this as well. 

**Cost:** Free

## Workflow Orchestration

If you can't accomplish everything with Fivetran, you need a workflow orchestration tool.  Similar to other tools on the market (Like Airflow), it's python based and allows you to pretty much do anything want.  It's free to use as well as has a great community.  Join their **Slack** channel and **Discourse** for additional help.

The only downside to this vs. more expensive tools, is you need to supply your own compute infrastructure for executing jobs.  Couple this with **AWS EC2**, **ECS**, or **Lambdas** and you're ready to go.  Prefect offers:

* Scheduling
* Retries
* Logging
* Caching
* Notifications
* Observability

**Cost:** Free

**URL**: [https://prefect.io](https://prefect.io)

## Business Intelligence (BI)

Preset is a Business Intelligence (BI) tool that is built on the Apache Open-Source project called [Superset](https://superset.apache.org).  It provides easy connectivity to Snowflake and a graphical explorer for working with data.  It allows you to crate what they refer to as **Virtual Data Sets** which is any SQL Query you want to run presented as a table.  You can then create **Dashboards** that are composed of these Virtual Data Sets.

**Cost:** Free

**URL**: [https://preset.io](https://preset.io)

## Notebook Environment

Mode offers a combination of both visualzation tools as well as a built in notebook environment.  You start by defining any query you'd like to select data from your warehouse, and then you can build visuals off of those queries or use them as a dataset which can be access directly as a Pandas dataframe.

**Note**: I didn't included this as a BI tool becuase I feel the SQL only access to data is a bit of a limiting function.  I prefer the way you can pre-package datasets in Preset.

**URL**: [https://preset.io](https://preset.io)

Hex

**URL**: [https://preset.io](https://preset.io)

**Cost:** Free

## Cloud Platform

AWS and it's magical consumption based pricing and free tier!

**Cost:** Consumption based with Generous Free Tier

**URL**: [https://aws.amazon.com/free/](https://aws.amazon.com/free/)

## Other Notable Mentions

* **VSCode**: Python, Git, Extensions, Debugging.  It's fantastic.  The best IDE out there.
* **GitHub**: Even if you're a single person, you should be using GitHub. Showcase your work and get used to the workflow.
* **Docker**: Grab Docker Desktop and the Docker Hub when you want to install various tools locally.  It saves a ton of time.

**Cost:** Free

## Conclusion

*If you liked what you read, [subscribe to my newsletter](https://campaign.dataknowsall.com/subscribe), and you will get my cheat sheet on Python, Machine Learning (ML), Natural Language Processing (NLP), SQL, and more. You will receive an email each time a new article is posted.*

## References

Containers Photo by <a href="https://unsplash.com/it/@timelabpro?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Timelab Pro</a> on <a href="https://unsplash.com/photos/sWOvgOOFk1g?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
  
  
  