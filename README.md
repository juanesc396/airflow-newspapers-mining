# airflow_scrapy_newspapers
The purpose of ​​this project is to automate an ETL which scrape all days headlines of Spanish-speaking newspapers in a MongoDB, save them and make maintainment through Airflow. Next, through nlp_task get the raw data in MongoDB, classify it and save it in MySQL into AWS RDS.


The tools I used for this project were:
- Airflow
- Scrapy
- MongoDB
- MySQL
- WSL2(Ubuntu)
- Celery
- Redis

The project is ejecuted into a WLS2 and Windows 10 OS. The databases are in Windows 10 and Airflow and Scrapy, into WSL2. 

To connect scripts, I created an environment variable, "IPPC", which store the ip of my Windows OS, where the MongoDB(to save the scraped data) and MySQL(to save the Airflow Credentials) databases are hosted. I edited the .bashrc file with...

```
export IPPC=$(grep -m 1 nameserver /etc/resolv.conf | awk '{print $2}')
```

I also added RDSIP and RDSPW, which allows me to get credentials to manage MySQL.

The next diagram represent how the task are organized.

[![na-airflow.png](https://i.postimg.cc/jdSktqKn/na-airflow.png)](https://postimg.cc/JtSQQLsR)
