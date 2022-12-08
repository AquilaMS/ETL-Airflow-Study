from datetime import timedelta
from airflow import DAG 
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from datetime import datetime
import study_etl as etl
import pandas as pd
import json
import client_api
import write_csv


etl.DATA_COUNT = int(Variable.get('STUDYETL_DATACOUNT'))

auth_admin = {
  'username': Variable.get('STUDYETL_API_USERNAME'),
  'password': Variable.get('STUDYETL_API_PASSWORD')
} 

def run_login(login_obj = auth_admin):
    result = client_api.login(login_obj)
    print(result)
    return result


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
    etl.execute_good_sql(df, auth_admin)
    

def insert_bad_data(ti):
    json_df = ti.xcom_pull(task_ids = 'run_etl')
    df = json.loads(json_df)
    etl.execute_bad_sql(df)

def write_data():
    write_csv.write_updated_data(auth_admin)

with DAG ('dag_study_etl_api', start_date = datetime(2022,1,1), schedule_interval='5 * * * *', catchup = False) as dag:
    run_login = PythonOperator(
        task_id = 'run_login',
        python_callable=run_login
    )
    run_etl = PythonOperator(
        task_id = 'run_etl',
        python_callable=run_etl_data,
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
    write_good_data = PythonOperator(
        task_id = 'write_data',
        python_callable=write_data,
        trigger_rule = 'none_failed_or_skipped'
    )
    run_login >> run_etl >> verify_integrity >> [insert_good, insert_bad] 
    insert_good >> write_good_data