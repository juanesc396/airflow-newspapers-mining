# airflow_scrapy_newspapers
The purpose of ​​this project is to automate an ETL which scrape all days headlines of Spanish-speaking newspapers in a MongoDB, save them and make maintainment through Airflow.


The tools I used for this project were:
- Airflow
- Scrapy
- MongoDB
- WSL2(Ubuntu)
- Celery
- Redis

The project is ejecuted into a WLS2 and Windows 10 OS. The databases are into Windows 10 and Airflow and Scrapy, into WSL2. The instructions are made to use the WLS2-Windows method.

To connect scripts, I created an environment variable, "IPPC", which store the ip of my Windows OS, where the MongoDB(to save the scraped data) and MySQL(to save the Airflow Credentials) databases are hosted. I edited the .bashrc file with...

```
export IPPC=$(grep -m 1 nameserver /etc/resolv.conf | awk '{print $2}')
```

To use this repo, you will install Python [Airflow](https://airflow.apache.org/docs/apache-airflow/stable/start.html) (2.4.3 version), Celery and Redis into a virtual environment, create the environment variable.

```
sudo apt update
sudo apt install python3

# in a folder
python3 -m venv airflowvenv
source airflowvenv/bin/activate

# Airflow needs a home. `~/airflow` is the default, but you can put it
# somewhere else if you prefer (optional)
export AIRFLOW_HOME=~/airflow

# Install Airflow using the constraints file
AIRFLOW_VERSION=2.4.3
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
# For example: 3.7
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example: https://raw.githubusercontent.com/apache/airflow/constraints-2.4.3/constraints-3.7.txt
sudo pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

pip install celery==5.2.7
pip install redis==4.4.0
```
Next, clone this repo, and execute airflow

```
redis-server
airflow celery worker
airflow scheduler
airflow webserver
```
In your navigator, you will manage Airflow through http://localhost:8080/home
