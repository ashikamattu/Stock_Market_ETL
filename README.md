# Stock_Market_ETL
This is a Stock market analysis project that fetches prices for each stock in VUG index from rapodapi.com and performs basic to advanced analytics with the data collected. There are two parts to this project 

Part 1 - Exploring various components of GCP to create a simple batch data pipeline that extracts data from an API everyday and loads into BigQuery via Cloud Function and DataFlow job and create a simple visualiztion on Looker Studio.

Part 2 - I am planning to use historical dataset to answer some interesting questions. Integrating Databricks/PySpark on GCP and performing  analytics is the main goal of this part. Eventually, I might perform incremental load and update the dashboard based on new data.

Part 1 - 

Tech Stack -
Python
SQL
GCP - GCS Bucket, IAM, Cloud Function, Dataflow, Google BigQuery, Looker Studio
AirFlow

This is the architecture diagram - 
![alt text](Architecture.png)

I ended up using airflow on my local machine (via docker) as Cloud COmposer seemed to be expensive

Overview - 

The airflow dag is scheduled to extract data from the API and upload the data to GCS bucket in csv format.
Once the dag run is complete, it would have uploaded the csv file to GCS bucket. 
The Cloud function triggers when a new file lands in the bucket and starts the corresponding dataflow job. 
The dataflow job uploads this new csv file into BigQuery table and from there you can visualize data and so on.


Airflow installation and execution steps through docker (Windows). Read through the end to avoid restarting -

1. Create a directory named airflow and inside that create three sub directories - logs, dags, plugins and place docker-compose.yaml file inside airflow directory
2. Install docker desktop for windows - https://docs.docker.com/desktop/setup/install/windows-install/. Launch the desktop app and make sure docker is running.
3. Download docker-compose.yaml file of airflow latest release - https://airflow.apache.org/docs/apache-airflow/2.10.5/docker-compose.yaml
4. In the airflow folder, **run "docker-compose up airflow-init". Navigate to docker desktop. It should look something like below -
![alt text](docker-container.jpg)
5. Once you see the containers on Docker Desktop, **run "docker-compose up" in the same directory and wait for docker more containers to be created. 
![alt text](airflow-webserver.jpg)
This creates a profile with username "airflow" with defualt password set to "airflow". Click on the arrow next to "8080:8080" to launch airflow UI
![alt text](airflow-UI.jpg)
6. Login using the default credentials and you will see list of dags on the home page.
![alt text](airflow-home.jpg)
7. Now you can place your dag.py file inside the "dags" folder that you created in step 1 and it appears on the UI after a while. For readability, create a "scripts" folder inside the "dags" folder and place "extract_to_gcs.py". We also need "tickers.csv" and ".env" files in there as the code depends on them. 
8. Navigate to the "fetch_stock_market_data" dag and monitor the dag.
9. Lastly, run "docker-compose down" from the airflow directory to stop the container.

*****IMPORTANT NOTE*****
Additionally, since we are executing the script through docker, it will not have access to the default google cloud credentials for the service account. For simplicity I chose to keep the application_default_credentials.json file in the dags folder and create a variable in docker-compose.yml file and set it to the application_default_credentials.json. ** Make this change before you run steps 4 and 5
![alt text](docker-compose-gcloud-creds.jpg)

