Title: How to Setup a Simple ETL Pipeline with AWS Lambda for Data Science
Date: 2023-02-09
Modified: 2023-02-09
Status: published
Tags: aws, datascience, python, data, etl, dataengineering
Slug: lambdaetl
Authors: Brian Roepke
Summary: How to setup a simple ETL pipeline with AWS Lambda that can be triggered via an API Endpoint or Schedule and write the results to an S3 Bucket for ingestion.
Description: How to setup a simple ETL pipeline with AWS Lambda that can be triggered via an API Endpoint or Schedule and write the results to an S3 Bucket for ingestion.
Header_Cover: images/covers/lamb.jpg
Og_Image: images/covers/lamb.jpg
Twitter_Image: images/covers/lamb.jpg

# What is AWS Lambda and Serverless Computing?

A Lambda function in AWS is a piece of code that is executed in response to an event.  The event can be a request to an API endpoint, a file being uploaded to an S3 bucket, or a scheduled event.  The code is executed in a container that is spun up on demand and then destroyed when the code has finished executing.  This is called serverless computing.

From [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html) Documentation:

>Lambda runs your function only when needed and scales automatically, from a few requests per day to thousands per second. You pay only for the compute time that you consume—there is no charge when your code is not running. For more information, see AWS Lambda Pricing.

A Lambda function is a wonderful way to think about ETL for smaller jobs that need to run frequently.  Such as on a trigger, like an API call, or nightly on a schedule.  It also allows you to orchestrate multiple Lambda functions together to create a more complex ETL pipeline.

Let's dive into creating our first Lambda function.

## Creating Your Lamba Function

From the AWS Console, navigate to the Lambda service.  Press the **Create Function** button to get started.  You will be prompted to select a blueprint.  For this example, we will select **Author from scratch**.  Give your name an approprite name and select **Python 3.9** as the runtime.  Select the **architecture** you prefer or typically develop locally on.  This makes it easier to upload new libraries that are compatible with your Lambda function.

![Creating a new function]({static}../../images/posts/lambdaetl_create_function.png)

You can create a **new role** or choose an **existing** one.  We'll cover that in the next section.

### Lamba Role

A critical part of creating a Lambda function is the **role**.  The **role** is what allows the function to access other AWS services.  For this example, we will need to give the function access to the **Lambda** and **S3**.  I also gave mine access to **VPC** but that's not necessary for this setup.

It's a good practice to create a new role to help you isolate only the permissions needed for this function.  Or if you will create multiple lambda functions for ETL use cases, you might want to consider a more generic naming like **Lamba-ETL-Role**.

![Role Configuration]({static}../../images/posts/lambdaetl_role.png)

### Set Your Function's Timeout

Next is configuring the functions timeout.  Depending on how long the function will take to execute, you can increase it to a maxium of 15 minutes.  For this example, we will set it to **1 minute**.  You will be able to see in your CloudWatch logs if the timeout was reached.

Click on the **Configuration** tab and under **General Configuration** set the timeout to 1 minute.

![Set Timeout]({static}../../images/posts/lambdaetl_timeout.png)


## Using the Parameters and Secrets Extension

Next - this isn't 100% necessary but it's a great practice when you want to ensure that you're handling sensitive data safely and not exposing it in your code.  In the past, i've wrtten about how to use [Environment Variables]({filename}../other/envvar.md) to do this locally, however in AWS we'll use the **Parameters and Secrets Extension**.

The **Parameters and Secrets Extension** allows you to store sensitive data in the AWS Secrets Manager and then access it in your Lambda function.  This is a great way to store API keys, database credentials, etc.  You can also use it to store non-sensitive data like configuration settings.  You can read up more on this functionaility here: [Configure the Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets_lambda.html)

We're going to start by adding a Layer to our Lambda function.  This will allow us to access the extension.  From the **Code** tab, scroll all the way to the bottom and click on **Add a Layer**.  Select **AWS Layers** and then choose **AWS-Parameters-and-Secrets-Lambda-Extension-Arm64** and the latest version of that layer.

![Add Parameters and Secrets Layer]({static}../../images/posts/lambdaetl_secrets.png)

Next we need to add code that will help us access the secrets.  I've added this to a small function that will look up my an **API Key** for [The Movie Database](https://www.themoviedb.org) (TMDB) and return it.  You can see the full code below.  TMDB is a great API for getting movie and TV show information and it's free to use for non-commercial purposes.

we'll create a `headers` varable with the JSON object as show below.  We'll then pass that into our API call to the **secrets_extension_endpoint** as shown.  The response will be a JSON object with the secret string.  We'll then parse that string and return the API key.

Where my code says **<< your secrets ARN >>** you'll need to replace that with the **ARN** of your secret.  You can find that in the **AWS Secrets Manager console**.

**Note:** *You will need to go back and modify your role to allow access to the secret you created.  You can find instructions on how to do that in the [AWS Documentation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples.html).  Follow the example in the section "Example Read one secret (attach to an identity)".*


```python
import requests
import json

def get_tmdb_api_key():

    headers = {"X-Aws-Parameters-Secrets-Token": os.environ.get("AWS_SESSION_TOKEN")}

    secrets_extension_endpoint = (
        "http://localhost:"
        + "2773"
        + "/secretsmanager/get?secretId="
        + "<< your secrets arn >>"
    )

    r = requests.get(secrets_extension_endpoint, headers=headers)
    secret = json.loads(r.text)["SecretString"]
    secret = json.loads(secret)
    TMDB_API_KEY = secret["TMDB_API"]

    return TMDB_API_KEY
```

## Add Support for Pandas

Next, our example and tons of other ETL use cases will require the use of Pandas.  We'll need to add a layer to our Lambda function to support this.  From the **Code** tab, scroll all the way to the bottom and click on **Add a Layer**.  Select **Custom Layers** and then choose **AWSSDKPandas-Python39-Arm64** and the latest version of that layer.

After enabling this layer, you can `import pandas` in your code *without* having to upload the package to your lambda function.

![Add Pandas Layer]({static}../../images/posts/lambdaetl_pandas.png)


## Writing Files to an S3 Bucket

One very powerful workflow with modern Data Warehouses / Platforms is the ability to directly work with JSON data.  We'll take advantage of this by outputting data to **JSON files** in an** S3 bucket**.

We'll create a function that will take a **DataFrame** and write it to a **JSON file** in an S3 bucket.  We'll use the `boto3` library to do this.  We'll create a JSON string from using Pandas `to_json` method, encode it as `utf-8`, and then write it to the S3 bucket.

```python
def write_to_s3(df, type, imdb_id):   
    
    # Get JSON for the DataFrame
    output = json.loads(df.to_json(orient='records'))
    
    string = str(output)
    encoded_string = string.encode("utf-8")

    bucket_name = "lambda-tmdb"
    file_name = "out.json"
    s3_path = "output/" + type + "/" + imdb_id + "-" + type + "-" + file_name

    s3 = boto3.resource('s3')
    object = s3.Object(bucket_name, s3_path)
    object.put(Body=encoded_string)
    
    return "Success"
```

We simply call this function when we're ready to output our DataFrame to S3 with a few parameters such as the **DataFrame** istelf, the **type** of data we're writing, and the **IMDB ID** of the movie or TV show.  The type is here for convenience so we can write different types of data with a single function while creating a unique file name for each movie lookup.

```python
write_to_s3(df_crew, "crew", imdb_id)
```

## Deploying Your Lambda Function

There are multiple ways to deploy your function.  The easiest is to use the AWS Console and upload a zip file.  However, adding a little bit of automation here will simplify your life when making changes to your code.  

The first step you'll need to do is set up the AWS CLI.  You can find instructions on how to do that in the AWS Documentation [Getting started with the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html).  You'll want to **create a new IAM user** with the appropirate permissions to write to the Lambda service.

Next, I wrote a simple `bash` script that i can call from my local terminal which does all the work needed.  One very important step in this is to zip up your python libraries at the correct level and package them with the zip file.  This shows you the process of changing to the `sites-packages` directory and zipping the contents of the libraries you want to keep.  Explicitly name the libraries you want here so that you don't end up uploading unnecessary files.

**Note:** *This also asssumes that I've created a local virtual environment and have my function code local as well. I prefer to build my Lambdas this way so that I can version control everything in GitHub*

```bash
# delete the old zip
rm tmdb-deployment-package.zip

# change the directory to the site-packagaes directory and zip the contents
cd venv/lib/python3.9/site-packages

# Explicitly add the tmdbsimple package folders needed for the lambda function
zip -r ../../../../tmdb-deployment-package.zip tmdbsimple tmdbsimple-2.9.1.dist-info

# change back to the root directory and add the needed python files
cd ../../../../
zip -g tmdb-deployment-package.zip lambda_function.py

# deploy to AWS Lambda
aws lambda update-function-code --function-name lambda-tmdb --zip-file fileb://tmdb-deployment-package.zip
```



![Post Deployment]({static}../../images/posts/lambdaetl_deploy.png)

## Monitoring the Lambda Function with CloudWatch

Add to “default” stage logging as CLF type

```text
$context.integrationErrorMessage
```

![Enable Logging for API Gateway Errors]({static}../../images/posts/lambdaetl_api_logging.png)


[Read more here](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-troubleshooting-lambda.html)


## Trigger the Lambda Function with an API Endpoint



![Create a new API]({static}../../images/posts/lambdaetl_create_api.png)


```text
?ids=tt0162346&ids=tt0326900
```

```json
{"ids" : ["tt0162346", "tt0326900"]}
```

## Conclusion



*If you liked what you read, [subscribe to my newsletter](https://campaign.dataknowsall.com/subscribe), and you will get my cheat sheet on Python, Machine Learning (ML), Natural Language Processing (NLP), SQL, and more. You will receive an email each time a new article is posted.*

## References

Lamb photo by <a href="https://unsplash.com/@rodlong?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Rod Long</a> on <a href="https://unsplash.com/photos/aJvSX36kweg?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
  
  