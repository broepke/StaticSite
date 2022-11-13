Title: Getting Started with Astromer Airflow - The Data Engineering Workhorse
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

We'll start here with **Airflow**. [Apache Airflow](https://en.wikipedia.org/wiki/Apache_Airflow) is an open-source workflow management platform that helps you build **Data Engineering Pipelines**. One of the biggest advantages to Airflow, and why it is so popular, is that you write your configuration in Python in the form of what is referred to as a DAG [Directed Acyclic Graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph)). The power of writing a DAG with Python means that you can leverage the powerful quite of Python libraries available to do nearly anything you want.

You can set up your Airflow instance on a cloud provider. You can even use the AWS version called [Amazon MWAA](https://aws.amazon.com/managed-workflows-for-apache-airflow/). This article will focus on the Astronomer Airflow managed service, one of the most popular ways to run Airflow.

Next up is **Astronomer**. [Astronmer](https://www.astronomer.io) is a managed **Airflow** service that allows you to orchestrate workflows in a cloud environment. A common use case for Airflow is building **Data Engineering Pipelines** and taking data from one source, transforming it over several steps, and loading it into a data warehouse. In this post, I'll walk through the basics of Airflow and how to get started with Astronomer.

Let's get started!

### Install Homebrew

Homebrew will be the easiest way for you to install the Astronomer CLI.  If you don't have Homebrew installed, you can install it by visiting the [Homebrew website](https://brew.sh/) and running the command they provide.

### Install Docker

Next, we need to install **Docker**. Docker is a **container** management system that allows you to run virtual environments on local computers and in the cloud. Docker is extremely lightweight and powerful. Airflow runs in docker containers and installs everything needed, such as a web server and a local database. Head to the Docker website and install [Docker Desktop](https://docs.docker.com/get-docker/) for your operating system.

*Note: Commercial use of Docker Desktop in larger enterprises (more than 250 employees OR more than $10 million in annual revenue) and government entities requires a paid subscription.*

### Astronomer CLI

Next, let's get [Astronomer CLI](https://docs.astronomer.io/astro/cli/install-cli) (Command Line Interface) installed. The CLI is a command line tool that allows you to interact with the Astronomer service. You can use the CLI to create new projects, deploy code, and manage users. 

```bash
brew install astro
```

**Note:** For this example, we're not going to publish any of our DAGs to the cloud; we'll run them locally to get a feeling for how Astronomer works.

### Create a Python Virtual Environment

A Virtual Environment is a great way to isolate the packages you'll use to run Airflow, allowing you to have multiple Airflow projects with different dependencies. You can create a virtual environment by running the following command:

```bash
python3 -m venv venv
```

And then activate the environment if necessary. If you're using Visual Studio Code, you can use the command palette to activate the environment, or it should activate as you open the project.

```bash
source venv/bin/activate
```

## Let's Get Started - Initialize a Project

Create a new folder for your project and launch your IDE of choice; my tool is Visual Studio Code. In this example, I called mine `Astro`, but a more descriptive name for the job you're trying to run would be more appropriate.

 Run the command `astro dev init`. This will create a new project with a few files and folders. The most important file is the **Dockerfile**. This file is used to build the docker image you will use to run the Airflow instance. The Dockerfile is a text file that contains all the commands a user could call on the command line to assemble an image. Using docker build, users can create an automated build that executes several command-line instructions in succession.

 You will also find a **requirements.txt** file in the folder that contains all the python packages you'll need to run your DAGs. You can add additional packages to this file as needed. As we get here, we'll not have any additional dependencies; the only one present will be `apache-airflow`.

## The Anatomy of a DAG

DAGs placed in the `/dags` directory will automatically appear in the Airflow UI. It's important that the `.py` file that contains the logic for the DAG has a DAG context manager definition; you can see the one below in the line `with DAG('example_dag'`. Newer versions of Airflow use decorators (`@dag(`) to accomplish the same thing.

Let's look at an example DAG and discuss the various components.


```python
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.version import version
from datetime import datetime, timedelta


def my_custom_function(ts,**kwargs):
    """
    This can be any python code you want and is called from the python 
    operator. The code is not executed until the task is run by the 
    airflow scheduler.
    """
    print(f"I am task number {kwargs['task_number']}. This DAG Run execution date is {ts} and the current time is {datetime.now()}")
    print('Here is the full DAG Run context. It is available because provide_context=True')
    print(kwargs)


# Default settings applied to all tasks
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Using a DAG context manager, you don't have to 
# specify the dag property of each task
with DAG('example_dag',
         start_date=datetime(2019, 1, 1),
         max_active_runs=3,
         schedule_interval=timedelta(minutes=30), 
         default_args=default_args,
         # catchup=False
         ) as dag:

    t0 = DummyOperator(
        task_id='start'
    )

    t1 = DummyOperator(
        task_id='group_bash_tasks'
    )
    t2 = BashOperator(
        task_id='bash_print_date1',
        bash_command='sleep $[ ( $RANDOM % 30 )  + 1 ]s && date')
    t3 = BashOperator(
        task_id='bash_print_date2',
        bash_command='sleep $[ ( $RANDOM % 30 )  + 1 ]s && date')

    # generate tasks with a loop. task_id must be unique
    for task in range(5):
        if version.startswith('2'):
            tn = PythonOperator(
                task_id=f'python_print_date_{task}',
                python_callable=my_custom_function,
                op_kwargs={'task_number': task},
            )
        else:
            tn = PythonOperator(
                task_id=f'python_print_date_{task}',
                python_callable=my_custom_function,
                op_kwargs={'task_number': task},
                provide_context=True,
            )


        t0 >> tn # inside loop so each task is added downstream of t0

    t0 >> t1
    t1 >> [t2, t3] # lists can be used to specify multiple tasks
```

* **Imports**: This is simply the list of python libraries you wish to utilize in your project.  Use these like you would any python project.
* **Custom Function**: Custom functions sit outside the context manger and are called from the Python Operator.  The function can be any python code you want and is called from the python operator. The code is not executed until the task is run by the airflow scheduler.
* **Default Arguments**: Default settings applied to all tasks.  These can be overridden at the task level.
* **Context Manager**: More on that next!

## Context Manager

The Context Manager 


## Start the Project

Run `astro dev start` to start the project. This will start the docker container.

If it doesn’t work, try `DOCKER_BUILDKIT=0 astro dev start`

```bash
[+] Running 4/4
 ⠿ Container astro_cf4ada-postgres-1   Started    0.7s
 ⠿ Container astro_cf4ada-scheduler-1  Started    1.5s
 ⠿ Container astro_cf4ada-triggerer-1  Started    1.5s
 ⠿ Container astro_cf4ada-webserver-1  Started     2.2s


Airflow is starting up! This might take a few minutes…
```

![Docker Desktop]({static}../../images/posts/astrointro_01.png)


After it completes the startup process, you'll see the following in your shell.  Note the URLs and credentials.

```bash
Airflow Webserver: http://localhost:8080
Postgres Database: localhost:5432/postgres
The default Airflow UI credentials are: admin:admin
The default Postgres DB credentials are: postgres:postgres
```



## Open and Explore the Airflow UI

After maybe 10 or 20 seconds you should be able to browse to the Airflow Admin UI at http://localhost:8080.



![Astro Home Page]({static}../../images/posts/astrointro_02.png)

![Astro DAG Home Page]({static}../../images/posts/astrointro_03.png)

![Astro DAG Graph]({static}../../images/posts/astrointro_04.png)


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



As always, the code for this article can be found on [GitHub](https://github.com/broepke/Astro)


*If you liked what you read, [subscribe to my newsletter](https://campaign.dataknowsall.com/subscribe) and you will get my cheat sheet on Python, Machine Learning (ML), Natural Language Processing (NLP), SQL, and more. You will receive an email each time a new article is posted.*

## References

Photo by <a href="https://unsplash.com/@nate_dumlao?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Nathan Dumlao</a> on <a href="https://unsplash.com/s/photos/astronomer?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>