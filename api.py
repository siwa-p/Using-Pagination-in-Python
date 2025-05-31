import requests
import json
import pandas as pd
import os
# get token using user-password dictionary
def get_token() -> dict:
    root_api = 'https://developyr-api.azurewebsites.net/api/auth'
    username = 'admin'
    password = 'password123'
    creds = {'username': username, 'password': password}
    headers = {'Content-Type': 'application/json'}

    response = requests.post(root_api, json=creds, headers=headers)

    print(response)
    if response.status_code == 200:
        json_data = response.json()
        print(json_data)
        with open('token.json','w') as f:
            json.dump(json_data,f)
        return json_data
    else:
        return "Unsuccessful"

# authenticate to the api using the token
def authenticate_api(keys_dict :dict = {}):
    
    with open('token.json') as f:
        token_dict= json.load(f)
    # token_dict = get_token()
    token = token_dict['token']
    root_api = 'https://developyr-api.azurewebsites.net/api/people'
    headers = {'Authorization': f'Bearer {token}'}
    # print(headers)
    response = requests.get(root_api, headers=headers, params=keys_dict)
    print(response)
    print(response.url)
    if response.status_code == 200:
        people_data = response.json()['data']
        # print(people_data)
        return people_data
    else:
        return "Unauthorized access"

    
# part 2
# add query string params offset and limit to the call
def query_added(offset, limit):
    keys_dict = {
                'offset' : offset, 
                 'limit' : limit
                 }
    people_data =  authenticate_api(keys_dict)
    # print(people_data)
    return people_data

# part 4
def cumulative_write():
    offset = 0
    limit = 10
    merged_dict = '['
    while True:
        data_queried = query_added(offset, limit)
        # this is a list of dictionaries
        # i need to merge into a single dictionary
        for data in data_queried:
            merged_dict = f'{merged_dict}{{'
            for index, (key,value) in enumerate(data.items()):
                # prevent comma at the end
                if index == len(data)-1:
                    merged_dict = f'{merged_dict}"{key}":"{repr(value).replace("'", "")}"'
                else:
                    merged_dict = f'{merged_dict}"{key}":"{repr(value).replace("'", "")}",'
            merged_dict = f"{merged_dict}}},"
        if not data_queried:
            break
        if not os.path.exists('output.json'):
            with open('output.json', 'w') as file:
                file.write(str(merged_dict))
        else:
            with open('output.json', 'a') as file:
                file.write(str(merged_dict))
        merged_dict = ''
        offset = offset + limit
    post_process('output.json')
    return None
         

# part 5
# read into a csv

def cumulative_write_csv():
    offset = 0
    limit = 10
    strings_to_add = "first_name, last_name, email, address \n"
    while True:
        data_queried = query_added(offset, limit)
        
        for data in data_queried:
            for index, (key, value) in enumerate(data.items()):
                if index ==len(data)-1:
                    strings_to_add = f'{strings_to_add} "{repr(value).replace("'", "")}"'
                else:
                    strings_to_add = f'{strings_to_add} "{value}",'
            strings_to_add = f"{strings_to_add} \n"
                
        
        if not data_queried:
            break
        
        if not os.path.exists('output.json'):
            with open('output.csv', 'w') as file:
                file.write(str(strings_to_add))
        else:
            with open('output.csv', 'a') as file:
                file.write(str(strings_to_add))
        strings_to_add = ''
        offset = offset + limit
        
    return None
        
def post_process(filepath):
    with open(filepath, 'r') as file:
        content = file.read()
        content = content[:-1] + ']'
    with open(filepath, 'w') as file:
        file.write(content)
    

def read_json(filepath):
    with open(filepath) as f:
        data = json.load(f)
        print(data)

def read_csv(filepath):
    # data = pd.read_csv(filepath)
    # print(data)
    with open(filepath, 'r') as f:
        data = f.read()
        print(data)


if __name__ == '__main__':
    # get_token()
    # authenticate_api()
    # query_added(2,10)
    # cumulative_write()
    cumulative_write_csv()
    # read_json('output.json')
    read_csv('output.csv')