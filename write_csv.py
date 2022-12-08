import csv
import requests
from datetime import datetime
import os
import client_api


timestamp = datetime.today().strftime('%Y-%m-%d')
hour = datetime.today().strftime('%H:%M:%S')

full_path = 'extracted/' + timestamp +'/'+ hour


def write_updated_data(auth_admin):

    token = client_api.login(auth_admin)
    headers = {"Authorization": 'Bearer ' + token}
    json_data = requests.get('http://localhost:8000/getallusers', headers=headers)

    print(json_data.status_code)
    if json_data.status_code == 200:
        if not os.path.exists('extracted'):
            os.mkdir('extracted')
        if not os.path.exists (str('extracted/' + timestamp)):
            os.mkdir(str('extracted/' + timestamp))
        if not os.path.exists(full_path):
            os.mkdir(full_path)
        with open(full_path + '/' + 'data.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(json_data)