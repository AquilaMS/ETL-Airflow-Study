from datetime import timedelta
from airflow import DAG 
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
import study_etl as etl
import pandas as pd
import json

def run_etl_data():
    gathered_data = pd.DataFrame(etl.get_data())
    print(gathered_data)
    return gathered_data.to_json()

def get_integrity(ti):
    json_df = ti.xcom_pull(task_ids = 'run_etl')
    df = json.loads(json_df)
    result = etl.verify_data_integrity(df)
    if result:
        return 'good_data'
    else:
        return 'bad_data'

def insert_good_data(ti):
    json_df = ti.xcom_pull(task_ids = 'run_etl')
    df = json.loads(json_df)
    etl.execute_good_sql(df)

def insert_bad_data(ti):
    json_df = ti.xcom_pull(task_ids = 'run_etl')
    df = json.loads(json_df)
    etl.execute_bad_sql(df)

with DAG ('minha_dag_de_estudo', start_date = datetime(2022,1,1), schedule_interval='5 * * * *', catchup = False) as dag:
    run_etl = PythonOperator(
        task_id = 'run_etl',
        python_callable=run_etl_data,
        dag=dag
    )
    verify_integrity = BranchPythonOperator(
        task_id = 'verify_integrity',
        python_callable=get_integrity
    )
    insert_good = PythonOperator(
        task_id = 'good_data',
        python_callable = insert_good_data,
    )
    insert_bad = PythonOperator(
        task_id ='bad_data',
        python_callable=insert_bad_data,
    )
    run_etl >> verify_integrity >> [insert_good, insert_bad]