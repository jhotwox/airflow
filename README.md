# airflow
Se trata de una herramienta de gestión, monitorización y planificación de flujos de trabajo como prefect

La forma de los flujos de esta herramienta se basan en DAGs (Grafos acíclicos dirigidos)

En esta actividad se obtendra la temperatura diariamene desde una API y se enviara un alerta en caso de que la temperatura sea mayor a 40°C

# Proceso
### Crear DAG
>Establecemos los argumentos por defecto
```python
default_args = {
    'owner': 'cristian',
    'retries': 1
}
```

>utilizamos with para crear DAG y establecemos:
- id con `dag_id`
- Una descripción con `description`
- Los argumentos que establecimos anteriormente con `default_ags`
- Cada cuanto se repetira con `schedule_interval`(en este caso diariamente porque utilizamos `@daily`)
- La fecha en la que se iniciara con `start_date`
- Si tomaremos en cuenta lo que no se hizo con `catchup`
```python
with DAG(
    dag_id='check_temperature',
    default_args=default_args,
    description='Check the temperature in Guadalajara',
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=True,
) as dag:
```
### Crear tareas
>Definimos las tareas dentro del DAG, envimos las respuestas de las otras tareas con `op_args` a través de XCom
```python
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
```

### Definir dependencias entre tareas (orden de ejecución)
```python
task_1 >> task_2 >> task_3
```

# Resultados
>Al presionar el boton "Trigger DAG podemos observar en la parte izquierda el estado de ejecución y al dar click a la tarea "fetch_data" podemos observar información especifica sobre esa tarea"
><img src="https://github.com/jhotwox/airflow/blob/main/2024-10-11_151526.png?raw=true">

>Tarea "get_temperature"
><img src="https://github.com/jhotwox/airflow/blob/main/2024-10-11_151548.png?raw=true">
>Logs "get_temperature" para observar la información que retorna la tarea
><img src="https://github.com/jhotwox/airflow/blob/main/2024-10-11_151637.png?raw=true">


>Tarea "check_temperature"
><img src="https://github.com/jhotwox/airflow/blob/main/2024-10-11_151626.png?raw=true">
>Logs "check_temperature" para observar la información que retorna la tarea
><img src="https://github.com/jhotwox/airflow/blob/main/2024-10-11_151645.png?raw=true">

#### Alerta
>Si forzamos que get_temperature retorne un valor mayor a 45 podemos observar la alerta
><img src="https://github.com/jhotwox/airflow/blob/main/2024-10-11_152033.png?raw=true">

#### Error
>Si forzamos un error en el fetch de datos podemos observar que la tarea fallo
><img src="https://github.com/jhotwox/airflow/blob/main/2024-10-11_153330.png?raw=true">