# Youtube API Data Ingestion

This project contain Airflow dag for data ingestion of the videos with "Power BI" and "Power Query" subject 
(from Youtube API)

## Description

Project contains dag and related files for fetching data from Youtube API by provided queries (in a scope of this task 
the queries are `Power BI` and `Power Query`). As per requirement of the technical task, those videos with less than 1000
channel subscribers should not be written to database. 

Current set dag schedule is daily. 
Besides dag files, project contains templates of sql scripts for further visualization of reports based on the stored 
data. Please check 'database-scripts' folder for more details  

## Getting Started

In order to locally run the application, the `Docker` should be installed on your local machine.
Please check official `Docker` [website](https://www.docker.com/) for more details.

After above-mentioned is done please proceed with steps below:
1. Clone project repository:
```
git clone https://github.com/EugeneVojtik/youtube_airflow_data_collector.git
```
2. Navigate to the project directory:
```
cd youtube_airflow_data_collector
```
3. Build docker-containers by the command:
```
docker-compose -f docker-compose.yaml build
```
Docker will start installation of required libs, images. It can take a while

4. Get Google services developer key. Please find more details by the next [link](https://cloud.google.com/docs/authentication/api-keys#console)

5. Export below-mentioned variables:
```
export DEVELOPER_KEY="YOUR_DEVELOPER_KEY_VALUE"
export AIRFLOW_DB_USER=""
export AIRFLOW_DB_PASSWORD=""
export ANALYTICS_DB_USER=""
export ANALYTICS_DB_PASSWORD=""
export ANALYTICS_DB_DATABASE=''
```

For a quick start please use below commands:
```
export DEVELOPER_KEY="YOUR_DEVELOPER_KEY_VALUE"
export AIRFLOW_DB_USER="airflow"
export AIRFLOW_DB_PASSWORD="airflow"
export ANALYTICS_DB_USER="root"
export ANALYTICS_DB_PASSWORD="root"
export ANALYTICS_DB_DATABASE='analytics'
```
* Please note, values of AIRFLOW_DB_USER and AIRFLOW_DB_PASSWORD variables will be used as a login on Airflow UI further. 

5. Up containers:
```
docker-compose -f docker-compose up
```
It will start all the related services.
After logs below Airflow UI is ready to proceed the requests:
```
airflow-webserver_1  | [2023-09-21 20:31:00 +0000] [14] [INFO] Listening at: http://0.0.0.0:8080 (14)
airflow-webserver_1  | [2023-09-21 20:31:00 +0000] [14] [INFO] Using worker: sync
airflow-webserver_1  | [2023-09-21 20:31:00 +0000] [26] [INFO] Booting worker with pid: 26
airflow-webserver_1  | [2023-09-21 20:31:00 +0000] [27] [INFO] Booting worker with pid: 27
airflow-webserver_1  | [2023-09-21 20:31:00 +0000] [28] [INFO] Booting worker with pid: 28
airflow-webserver_1  | [2023-09-21 20:31:00 +0000] [29] [INFO] Booting worker with pid: 29

```

6. Go to "http://localhost:8080" for accessing Airflow UI. 
Use credentials mentioned in the note of point #4

7. Unpause dag and run it manually if required

