from airflow import DAG
import sys
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
#from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta
#from docker.types import Mount

def safe_main_callable():
    print("This is a safe main callable function.")
    from api_requests.insert_record import main
    return main()

default_args = {
    'description': 'ETL DAG for Weather Data',
    'start_date': datetime(2025, 12, 10),
    'catchup': False,}

# Definisi DAG Paling Sederhana
with DAG(
    dag_id='api-wheather-data-orchestrator',
    default_args=default_args,
    schedule=timedelta(minutes=1),
    catchup=False
) as dag:

    # Task cuma bilang Hello
    task_1 = PythonOperator(
        task_id='api-weather-ingest',
        python_callable=safe_main_callable
    )
    task_2 = BashOperator(
        task_id='dbt-weather-transformation',
        bash_command='dbt run --profiles-dir /opt/airflow/dbt --project-dir /opt/airflow/dbt/weather_dbt'
    )

    # Mengatur urutan: task_1 selesai dulu, baru task_2 jalan
    task_1 >> task_2