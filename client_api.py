import requests
import json

login_url = 'http://localhost:8000/login/'
add_good_url = 'http://localhost:8000/add/'

def parse_data(data):
  json_load= json.loads(data)
  stored_data = []
  rows = len(json_load['user_id'])
  actual_row = -1

  while actual_row <= rows-2:
    actual_row = actual_row +1
    stored_data.append(
      
      {
         'user_id': json_load['user_id'][str(actual_row)],
         'name': json_load['name'][str(actual_row)],
         'email': json_load['email'][str(actual_row)],
         'gender': json_load['gender'][str(actual_row)],
         'phone': json_load['phone'][str(actual_row)],
         'city': json_load['city'][str(actual_row)],
         'timestamp': json_load['timestamp'][str(actual_row)],
      }
     
    )
  return stored_data
  
def insert_with_api(login_obj, data):
  parsed_data = parse_data(data)
  print(parsed_data)
  token = login(login_obj)
  headers = {"Authorization": 'Bearer ' + token}
  rows = len(parsed_data)
  actual_rows = -1

  while actual_rows <= rows-2:
    actual_rows =actual_rows+1
    log = requests.post(add_good_url ,json=parsed_data[actual_rows], headers=headers)

  return (print(log.content))

def login(login_obj):
  log = requests.post(login_url, json = login_obj)
  if log.status_code == 200:
    return log.json()
  else:
    print('Wrong password/username')
    raise Exception('Wrong password/username')
    
#if 1==1:
  #insert_with_api(auth_admin, df_fake)
  #parse_data(df_fake)
