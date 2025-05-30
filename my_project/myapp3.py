import requests
import json

URL = "http://127.0.0.1:8000/userapi/userinfo/"
# URL = "http://127.0.0.1:8000/postapi/postinfo/"


def get_data(id=None):
    data = {}
    if id is not None:
        data = {'id': id}
    json_data = json.dumps(data)
    # create a header to tell the django that the data is in json format
    headers = {'content-Type': 'application/json'}
    r = requests.get(url=URL, headers=headers, data=json_data)
    data = r.json()
    print(data)

# get_data()


def post_data():
    data = {
        'username': 'aditya',
        'email': 'abhay@gmail.com',
        'is_staff': False,
    }

    headers = {'content-Type': 'application/json'}
    json_data = json.dumps(data)
    r = requests.post(url=URL, headers=headers, data=json_data)
    data = r.json()
    print(data)


# post_data()


def update_data():
    data = {
        'id': 16,
        'username': 'Suman',
        'is_staff': False
    }

    # convert it into json
    json_data = json.dumps(data)
    # specify the content type in header
    headers = {'content-Type': 'application/json'}
    r = requests.put(url=URL, headers=headers, data=json_data)

    data = r.json()
    print(data)


# update_data()

def delete_data():
    data = {'id': 15}
    # convert data into json string
    json_data = json.dumps(data)

    # specify content type in headers
    headers = {'content-Type': 'application/json'}

    # sending delete request to delete the object
    r = requests.delete(url=URL, headers=headers, data=json_data)


    # parsing json string to native python data type
    data = r.json()

    print(data)

delete_data()