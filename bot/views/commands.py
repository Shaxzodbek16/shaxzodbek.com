from base_url import BASE_URL
import requests


def create_commands(**kwargs) -> str:
    url = BASE_URL + '/user_commands/'
    try:
        requests.post(url, data=kwargs)
    except Exception as e:
        return str(e)
    return 'Command created successfully'
