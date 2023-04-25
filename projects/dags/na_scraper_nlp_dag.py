from airflow.decorators import task, dag
from airflow.operators.bash import BashOperator
from airflow.sensors.python import PythonSensor
from airflow.sensors.bash import BashSensor

from datetime import datetime
from default_args import default_args
from db_actions import mongodb_check


@dag(
    'newspaper_scraper_dag',
    default_args = default_args,
    description = 'A scraper that extract data from newspapers',
    schedule_interval='0 8 * * *',
    start_date = datetime(2023, 4, 10),
    catchup = False,
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

    nlp_task = BashOperator(
        task_id='nlp_task',
        bash_command='cd /home/juan/airflow; source venv/bin/activate; python3 projects/nlp_task/categorization.py'
    )

    mongo_sensor >> [ar_scraper, cl_scraper, es_scraper, mx_scraper, ur_scraper] >> nlp_task
newspaper_scraper_dag()