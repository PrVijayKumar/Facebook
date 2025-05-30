import requests
import json
import datetime

URL = "http://127.0.0.1:8000/postapi/postinfo/"

# r = requests.get(url = URL)
# data = r.json()

# print(data)


def get_data(id=None):
    data = {}
    if id is not None:
        data = {'id': id}
    json_data = json.dumps(data)
    headers = {'content-Type': 'application/json'}
    r = requests.get(url=URL, data=json_data, headers=headers)
    data = r.json()
    print(data)


# get_data(58)

def post_data():
    data = {
        'post_title': 'MP Police',
        'post_description': 'Bhopal is the capital of Madhya Pradesh',
        'post_date': str(datetime.datetime.now()),
        'post_user_id': '2',
    }
    # Convert python data into json data
    json_data = json.dumps(data)
    # add a header to the request
    headers = {'content-Type': 'application/json'}
    # send request and get responst
    r = requests.post(url=URL, headers=headers, data=json_data)
    # conver json response into python data
    data = r.json()
    # print(type(data))
    print(data)

# post_data()

def update_data():
    data = {
        'id': 98,
        'post_title': 'Nice article',
        # 'post_description': 'I am proud to be an Indian',
        'post_user_id': 2
    }

    # convert dict to json string
    json_data = json.dumps(data)

    # specify content type in headers
    headers = {'content-Type': 'application/json'}

    # make put request
    r = requests.put(url=URL, headers=headers, data=json_data)

    #parse json reponse
    data = r.json()

    print(data)


# update_data()

def delete_data():
    data = {'id': 97}

    # parse dict into json
    json_data = json.dumps(data)

    # specify content type in headers
    headers = {'content-Type': 'application/json'}

    # making delete request
    r = requests.delete(url=URL, headers=headers, data=json_data)

    # parsing json data into python native data
    data = r.json()

    print(data)


delete_data()

# def get_data(id=None):
#     data = {}
#     if id is not None:
#         data = {'id': id}
    
#     json_data = json.dumps(data)

#     r = requests.get(url=URL, data=json_data)

#     data = r.json()

#     print(data)


# get_data(58)