from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from extract import extract_data
from transform import transform_data
from load import load_data

default_args = {"owner": "airflow", "start_date": datetime(2025, 3, 21)}

with DAG("train_schedule_etl", default_args=default_args, schedule_interval="@daily", catchup=False) as dag:
    extract_task = PythonOperator(task_id="extract", python_callable=extract_data)
    transform_task = PythonOperator(task_id="transform", python_callable=transform_data)
    load_task = PythonOperator(task_id="load", python_callable=load_data)

    extract_task >> transform_task >> load_task
