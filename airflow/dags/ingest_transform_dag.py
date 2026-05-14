from airflow import DAG
from airflow.operators.python import PythonOperator  # correct for 2.7+
from datetime import datetime
import subprocess
import os

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")

def generate_data():
    subprocess.run(["python3", f"{PROJECT_ROOT}/scripts/generate_data.py"], cwd=PROJECT_ROOT)

def ingest_to_bigquery():
    subprocess.run(["python3", f"{PROJECT_ROOT}/scripts/ingest_to_bigquery.py"], cwd=PROJECT_ROOT)

def run_dbt_models():
    dbt_path = os.path.join(PROJECT_ROOT, "dbt")
    subprocess.run(["dbt", "run"], cwd=dbt_path)

def run_dbt_tests():
    dbt_path = os.path.join(PROJECT_ROOT, "dbt")
    subprocess.run(["dbt", "test"], cwd=dbt_path)

with DAG(
    "ingest_transform_dag",
    start_date=datetime(2026, 2, 3),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    
    task_generate = PythonOperator(
        task_id="generate_data",
        python_callable=generate_data
    )

    task_ingest = PythonOperator(
        task_id="ingest_to_bigquery",
        python_callable=ingest_to_bigquery
    )

    task_run_models = PythonOperator(
        task_id="run_dbt_models",
        python_callable=run_dbt_models
    )

    task_run_tests = PythonOperator(
        task_id="run_dbt_tests",
        python_callable=run_dbt_tests
    )

    task_generate >> task_ingest >> task_run_models >> task_run_tests
