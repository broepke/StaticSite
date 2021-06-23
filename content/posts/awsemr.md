Title: Setting Up AWS EMR with Jupyter Notebooks
Date: 2021-06-23
Modified: 2021-06-23
Category: AWS
Tags: aws, datascience, python, bigdata
Slug: awsemr
Authors: Brian Roepke
Summary: A setup guide for configuring AWS EMR with Spark and Jupyter Notebooks
Header_Cover: images/colliseum.jpg

## Basic Steps

1. Create a non-root IAM account for use with this process
2. Create a cluster with all components needed to run Notebooks and Spark
3. Create a new Notebook attached to the Cluser
4. Run analysis
5. Stop Notebook
6. Terminate the cluster

## Step 1: Creating a new IAM User

It's important to not use the root account for this process.  In most cases, the Notebook environment will fail to start/attach to the Python or PySpark kernels after initializing.  To overcome this, create the account with the appropriate permissions.  I used the following as a generic catch all, I didn't try to get to the bare minimum.

![AWS IAM User](images/awsemr-1.png)

## Create a new Cluster

![AWS IAM User](images/awsemr-2.png)

## Create a new Notebook

![AWS IAM User](images/awsemr-3.png)