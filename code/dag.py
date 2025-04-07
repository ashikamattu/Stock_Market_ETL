from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
import os

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
    'depends_on_past': False,
    'email': ['ashikamatt1@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('fetch_stock_market_data',
          default_args=default_args,
          description='Execute a Python script that loads data from API to GCS',
          schedule_interval='@daily',
          catchup=False)

with dag:
    dag_folder = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(dag_folder, 'scripts', 'extract_to_gcs.py')
    run_script_task = BashOperator(
        task_id='run_script',
        bash_command=f'python {script_path}',
    )