from airflow import DAG
from airflow.decorators import task, dag
from airflow.operators.bash import BashOperator
from airflow.sensors.python import PythonSensor

import pendulum
from datetime import timedelta
from default_args import default_args
from mongodb_actions import mongodb_check
@dag(
    'newspaper_scraper_dag',
    default_args = default_args,
    description = 'A scraper that extract data from newspapers',
    schedule = timedelta(days=1),
    start_date = pendulum.datetime(2022, 12, 12, tz="UTC"),
    tags=['scraper', 'nlp-project'],
)
def newspaper_scraper_dag():
    mongo_sensor = PythonSensor(task_id="mongodb_sensor", python_callable=mongodb_check)

    ar_scraper = BashOperator(
        task_id="ar_scraper",
        bash_command='cd; python3 airflow/projects/scraper/spiders/ar_newspaper_scraper.py',
    )
        
    cl_scraper = BashOperator(
        task_id="cl_scraper",
        bash_command='cd; python3 airflow/projects/scraper/spiders/cl_newspaper_scraper.py',
    )

    es_scraper = BashOperator(
        task_id="es_scraper",
        bash_command='cd; python3 airflow/projects/scraper/spiders/es_newspaper_scraper.py',
    )

    mx_scraper = BashOperator(
        task_id="mx_scraper",
        bash_command='cd; python3 airflow/projects/scraper/spiders/mx_newspaper_scraper.py',
    )

    ur_scraper = BashOperator(
        task_id="ur_scraper",
        bash_command='cd; python3 airflow/projects/scraper/spiders/ur_newspaper_scraper.py',
    )

    mongo_sensor >> [ar_scraper, cl_scraper, es_scraper, mx_scraper, ur_scraper]
newspaper_scraper_dag()