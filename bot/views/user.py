import json
from .base_url import BASE_URL
import requests


def create_user(**kwargs) -> str:
    url = BASE_URL + '/create_user/'
    user_id = kwargs.get('user_id')
    response = json.loads(requests.get(url).text)
    user_exists = False
    for i in response['results']:
        if i['user_id'] == kwargs['user_id']:
            user_exists = True
            requests.put(url + f'{user_id}/', data=kwargs)
            break
    if not user_exists:
        requests.post(url, data=kwargs)
        return 'User created successfully'
    return 'User already exists'
