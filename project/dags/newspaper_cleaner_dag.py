from airflow.decorators import dag
from airflow.sensors.python import PythonSensor
from airflow.operators.python import PythonOperator


import pendulum
from datetime import timedelta
from default_args import default_args
from mongodb_actions import mongodb_check
from mongodb_actions import clean_duplicates

@dag(
    'newspaper_clean_duplicates',
    default_args = default_args,
    description = 'A scraper that extract sadasd from newspapers',
    schedule = timedelta(days=7),
    start_date = pendulum.datetime(2022, 12, 12, tz="UTC"),
    tags=['scraper', 'nlp-project', 'test'],
    max_active_runs = 1
)
def cleaner():
    mongo_sensor = PythonSensor(
        task_id="success_sensor_python",
        python_callable = mongodb_check
        )

    newspaper_clean_duplicates = PythonOperator(
        task_id="database_cleaner",
        python_callable = clean_duplicates,
        )

    mongo_sensor >> newspaper_clean_duplicates
cleaner()