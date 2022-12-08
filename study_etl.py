import requests 
import sqlalchemy
import pandas as pd
from datetime import datetime 
import sqlite3
from sqlalchemy.orm import sessionmaker
import client_api
from fastapi.encoders import jsonable_encoder
import os

RANDOM_USER_URL = 'https://randomuser.me/api/'
DATA_COUNT = None
DATABASE_LOCATION = os.environ['SQLALCHEMY_DATABASE_URL']

stored_data = []

def validate_data(df: pd.DataFrame):
    
    if df.empty:
        raise Exception('Dataframe is empty')
    if pd.Series(df['user_id']).is_unique:
        pass
    else:
        return False
    if df.isnull().values.any():
        return False
    if df.isna().values.any():
        return False

    return True

def get_data():
    for count in range(DATA_COUNT):
        response_users = requests.get(RANDOM_USER_URL).json()
        response_users_results = response_users['results'][0]

        user_name = response_users_results['name']['first'] + ' ' + response_users_results['name']['last']
        user_city = response_users_results['location']['city']
        user_email = response_users_results['email']
        user_phone =response_users_results['phone']
        user_gender = response_users_results['gender']
        user_timestamp = datetime.now().strftime('%Y-%m-%d')
        user_id = datetime.now().strftime('%Y%m%d%H%S%f')
        
        user_data = {
            'user_id' : user_id,
            'name' : user_name,
            'email': user_email,
            'gender': user_gender,
            'phone': user_phone,
            'city' : user_city,
            'timestamp': user_timestamp
        }

        stored_data.append(user_data)
       
    if count == DATA_COUNT - 1:
        return stored_data
   
def verify_data_integrity(stored_data):
        user_dataframe = pd.DataFrame(stored_data)
        if validate_data(user_dataframe):
            return True           
        else:
            return False
        

def execute_good_sql(user_dataframe, auth_admin):
    df = pd.DataFrame(user_dataframe)
    #print(df)
    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()

    good_sql_query = """
        CREATE TABLE IF NOT EXISTS tb_users(
        user_id VARCHAR(200) PRIMARY KEY,
        name VARCHAR(200),
        email VARCHAR(200),
        gender VARCHAR(200),
        phone VARCHAR(200),
        city VARCHAR(200),
        timestamp VARCHAR(200)
        )
       """
    cursor.execute(good_sql_query)
    try:
        log = client_api.insert_with_api(auth_admin, df.to_json())
        print(log)
    except:
        print('Error batch')
    conn.close()

def execute_bad_sql(user_dataframe):
    df = pd.DataFrame(user_dataframe)
    print(df)
    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('users.sqlite')
    cursor = conn.cursor()

    bad_sql_query = """
        CREATE TABLE IF NOT EXISTS junk_tb_users(
        user_id VARCHAR(200) PRIMARY KEY,
        name VARCHAR(200),
        email VARCHAR(200),
        gender VARCHAR(200),
        phone VARCHAR(200),
        city VARCHAR(200),
        timestamp VARCHAR(200)
        )
       """
    
    cursor.execute(bad_sql_query)
    try:
        df.to_sql('junk_tb_users', engine, index = False, if_exists = 'append')
    except:
            print('Bad bad batch')
    conn.close()