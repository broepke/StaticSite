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



## Prerequisites

[Homebrew](https://brew.sh)
[Docker Desktop](https://docs.docker.com/get-docker/)

*Commercial use of Docker Desktop in larger enterprises (more than 250 employees OR more than $10 million USD in annual revenue) and in government entities requires a paid subscription.*

## Astronomer CLI

[Astronomer CLI](https://docs.astronomer.io/astro/cli/install-cli)

`brew uninstall astro`


## Virtual Environment


`python -m pip install --user virtualenv`


Virtualenv has one basic command: `virtualenv venv`. This will create a python virtual environment of the same version as virtualenv, installed into the subdirectory venv.

`source venv/bin/activate`

## Initialize a Project


create a new folder and run `astro dev init`. This will create a new project with a few files and folders. The most important file is the Dockerfile. This file is used to build the docker image that will be used to run the Airflow instance. The Dockerfile is a text file that contains all the commands a user could call on the command line to assemble an image. Using docker build users can create an automated build that executes several command-line instructions in succession.


## Start the Project

Run `astro dev start` to start the project. This will start the docker container.

If it doesn’t work, try `DOCKER_BUILDKIT=0 astro dev start`

## Open the Airflow UI

After maybe 10 or 20 seconds you should be able to browse to the Airflow Admin UI at http://localhost:8080.


## The Anatomy of a DAG

DAGs placed in the dags/ directory will automatically appear in the Airflow UI.  The DAG will not show up unless you define a DAG in the .py file that you will create.


```python
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.version import version
from datetime import datetime, timedelta


def my_custom_function(ts,**kwargs):
    """
    This can be any python code you want and is called from the python operator. The code is not executed until
    the task is run by the airflow scheduler.
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

# Using a DAG context manager, you don't have to specify the dag property of each task
with DAG('example_dag',
         start_date=datetime(2019, 1, 1),
         max_active_runs=3,
         schedule_interval=timedelta(minutes=30),  # https://airflow.apache.org/docs/stable/scheduler.html#dag-runs
         default_args=default_args,
         # catchup=False # enable if you don't want historical dag runs to run
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
                python_callable=my_custom_function,  # make sure you don't include the () of the function
                op_kwargs={'task_number': task},
            )
        else:
            tn = PythonOperator(
                task_id=f'python_print_date_{task}',
                python_callable=my_custom_function,  # make sure you don't include the () of the function
                op_kwargs={'task_number': task},
                provide_context=True,
            )


        t0 >> tn # indented inside for loop so each task is added downstream of t0

    t0 >> t1
    t1 >> [t2, t3] # lists can be used to specify multiple tasks
```


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