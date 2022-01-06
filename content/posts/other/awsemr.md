Title: Setting Up AWS EMR with Jupyter Notebooks
Date: 2021-06-22
Modified: 2021-06-22
Tags: aws, datascience, python, data
Slug: awsemr
Authors: Brian Roepke
Summary: A setup guide for configuring AWS EMR with Spark and Jupyter Notebooks
Header_Cover: images/covers/computer.jpg
Og_Image: images/covers/computer.jpg
Twitter_Image: images/covers/computer.jpg

## Basic Steps

1. Create a non-root IAM account for use with this process
2. Create a cluster with all components needed to run Notebooks and Spark
3. Create a new Notebook attached to the Cluster
4. Run analysis
5. Stop Notebook
6. Terminate the Cluster

## Step 1: Creating a new IAM User

It's important not to use the root account for this process.  In most cases, the Notebook environment will fail to start/attach to the Python or PySpark kernels after initializing.  To overcome this, create the account with the appropriate permissions.  I used the following as a generic catch-all; I didn't try to get to the bare minimum.

![AWS IAM User]({static}../../images/posts/awsemr-1.png)

## Create a new Cluster

Next, you want to create a new cluster.  The image below shows all of the relevant settings you can access through the **Advanced Configuration** Options.  You can add others as well, but these are the items—specifically the two Jupyter entries and Livy, which is a restful service for Spark.

Step through to the final page and make sure you select a PEM file that you will associate with the cluster.  It will be important to access the user interfaces for Hadoop, Hue, Spark, etc.

![AWS IAM User]({static}../../images/posts/awsemr-2.png)

## Create a new Notebook

Next, `Create Notebook` in EMR.  While you can create a cluster for yourself, it's important to select the one you just created. Use the `Choose existing cluster` option. This process will allow you to kill the cluster, and in turn, re-create it without losing data and the ability to continue coding on your cluster/Notebook.

![AWS IAM User]({static}../../images/posts/awsemr-3.png)

## After Analysis - Terminating

You can very easily build up a very large bill with EMR and clusters.  You must stop the Notebook and Terminate the cluster.

1. First, `stop` the Notebook but do not delete it.
2. Second, `terminate` the cluster.  It's not possible to stop them, but you can recreate them later.

## Continuing Your Analysis

When you're ready to continue with your analysis, simply `Clone` the cluster and wait for it to start.  Then return to the Notebook from earlier, and then use the `Change Cluster` button at the top to associate it with your newly cloned cluster.  

That's it.  Launch your Notebook and continue!

*If you liked what you read, [subscribe to my newsletter](https://campaign.dataknowsall.com/subscribe) and you will get my cheat sheet on Python, Machine Learning (ML), Natural Language Processing (NLP), SQL, and more. You will receive an email each time a new article is posted.*