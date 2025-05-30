import requests
import json
# URL = "http://127.0.0.1:8000/postapi/createpost/"
URL = "http://127.0.0.1:8000/postapi/postinfo/"

post_info = {
    'post_title': 'Post about India',
    'post_description': 'Patriotric Post',
    'post_user_id': 1,
}

json_data = json.dumps(post_info)
headers = {'content-Type': 'application/json'}
data = requests.post(url=URL, headers=headers, data=json_data)

json_data = data.json()

print(json_data)