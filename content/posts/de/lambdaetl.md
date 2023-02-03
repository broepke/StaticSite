Title: How to Setup a Simple ETL Pipeline with AWS Lambda for Data Science
Date: 2023-02-05
Modified: 2023-02-05
Status: draft
Tags: aws, datascience, python, data, etl, dataengineering
Slug: lambdaetl
Authors: Brian Roepke
Summary: How to setup a simple ETL pipeline with AWS Lambda that can be triggered via an API Endpoint and write the results to an S3 Bucket.
Description: How to setup a simple ETL pipeline with AWS Lambda that can be triggered via an API Endpoint and write the results to an S3 Bucket.
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




![Creating a new function]({static}../../images/posts/lambdaetl_create_function.png)

For now, skip adding a VPC.  We will create one shortly and attach it to the function.

### Lamba Role

A critical part of creating a Lambda function is the role.  The role is what allows the function to access other AWS services.  For this example, we will need to give the function access to the Lambda service, S3, and CloudWatch Logs.

It's a good practice to create a new role to help you isolate only the permissions needed for this function.

![Role Configuration]({static}../../images/posts/lambdaetl_role.png)

### Set Your Function's Timeout



![Set Timeout]({static}../../images/posts/lambdaetl_timeout.png)


## Using the Parameters and Secrets Extension

[Configure the Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets_lambda.html)


![Add Parameters and Secrets Layer]({static}../../images/posts/lambdaetl_secrets.png)


```python
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



![Add Pandas Layer]({static}../../images/posts/lambdaetl_pandas.png)


## Writing Files to an S3 Bucket


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


```python
write_to_s3(df_crew, "crew", imdb_id)
```


## Deploying Your Lambda Function

[Getting started with the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)

```bash
# delete the old zip
rm tmdb-deployment-package.zip

# change the directory to the site-packagaes directory and zip the contents
cd venv/lib/python3.9/site-packages

# Explicitly add the tmdbsimple package folders needed for the lambda function
zip -r ../../../../tmdb-deployment-package.zip tmdbsimple tmdbsimple-2.9.1.dist-info

# change back to the root directory and add the needed python files
cd ../../../../
zip -g tmdb-deployment-package.zip lambda_function.py lambda_helper_functions.py

# deploy to AWS Lambda
aws lambda update-function-code --function-name my-test-function --zip-file fileb://tmdb-deployment-package.zip
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
  
  