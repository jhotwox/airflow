# Python interpreter: /home/jhon/.local/pipx/venvs/venvs/apache-airflow/bin/python3
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import requests

def fetch_data():
    latitud = 20.62445
    longitud = -103.23423
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitud}&longitude={longitud}&current_weather=true"
    response = requests.get(url)
    return response.json()

def get_temperature(data):
    return data["current_weather"]["temperature"] 

def check_temperature(temperature):
    if temperature < 15:
        print("Hace frío")
    elif temperature > 28 and temperature < 40:
        print("Hace calor")
    elif temperature >= 40:
        print("Alerta! Hace mucho calor")
    else:
        print("El clima es agradable")

# definir el DAG
default_args = {
    'owner': 'cristian',
    'retries': 1
}
    
with DAG(
    dag_id='check_temperature',
    default_args=default_args,
    description='Check the temperature in Guadalajara',
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=True,
) as dag:
    # Definir las tareas
    task_1 = PythonOperator(
        task_id = "fetch_data",
        python_callable=fetch_data
    )
    task_2 = PythonOperator(
        task_id = "get_temperature",
        python_callable=get_temperature,
        op_args=[task_1.output]
    )
    task_3 = PythonOperator(
        task_id = "check_temperature",
        python_callable=check_temperature,
        op_args=[task_2.output]
    )
    
    # Dependencias entre tareas
    task_1 >> task_2 >> task_3