Title: A Quick Introduction to Astromer Airflow
Date: 2022-12-11
Modified: 2022-12-11
Status: draft
Tags: analytics, datascience, databases, dataengineering
Slug: astrointro
Authors: Brian Roepke
Summary: xxxx
Description: xxx
Header_Cover: images/covers/astro.jpg
Og_Image: images/covers/astro.jpg
Twitter_Image: images/covers/astro.jpg

# What is Astromer Airflow?



## Docker

[Docker Desktop](https://www.docker.com/products/docker-desktop/)



## Astronomer CLI


[Astronomer CLI](https://docs.astronomer.io/astro/cli/install-cli)

`brew uninstall astro`


## Virtual Environment


`python -m pip install --user virtualenv`


Virtualenv has one basic command:

`virtualenv venv`

This will create a python virtual environment of the same version as virtualenv, installed into the subdirectory venv.

`source venv/bin/activate`

## Initialize a Project


create a new folder and run `astro dev init`. This will create a new project with a few files and folders. The most important file is the Dockerfile. This file is used to build the docker image that will be used to run the Airflow instance. The Dockerfile is a text file that contains all the commands a user could call on the command line to assemble an image. Using docker build users can create an automated build that executes several command-line instructions in succession.


## Start the Project

Run `astro dev` start to start the project. This will start the docker container.

If it doesn’t work, try `DOCKER_BUILDKIT=0 astro dev start`

## Open the Airflow UI

After maybe 10 or 20 seconds you should be able to browse to the Airflow Admin UI at http://localhost:8080.


## The Anatomy of a DAG

DAGs placed in the dags/ directory will automatically appear in the Airflow UI.  The DAG will not show up unless you define a DAG in the .py file that you will create.


## Stop the Project

You can stop everything running with `astro dev stop`

```bash
❯ astro dev stop
[+] Running 4/4
 ⠿ Container astro_cf4ada-triggerer-1  Stopped
 ⠿ Container astro_cf4ada-webserver-1  Stopped
 ⠿ Container astro_cf4ada-scheduler-1  Stopped
 ⠿ Container astro_cf4ada-postgres-1   Stopped
 ```

## Conclusion



*If you liked what you read, [subscribe to my newsletter](https://campaign.dataknowsall.com/subscribe) and you will get my cheat sheet on Python, Machine Learning (ML), Natural Language Processing (NLP), SQL, and more. You will receive an email each time a new article is posted.*

## References

Photo by <a href="https://unsplash.com/@nate_dumlao?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Nathan Dumlao</a> on <a href="https://unsplash.com/s/photos/astronomer?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>