import requests
from base_url import BASE_URL


def create_feedback(**kwargs) -> str:
    url = BASE_URL + '/feedback/'
    with open(kwargs['file'], 'rb') as f:
        files = {'file': f}
        res = requests.post(url, data=kwargs, files=files)

    if res.status_code == 201:
        return 'Feedback created successfully'
    else:
        return f"Failed to create feedback: {res.status_code} - {res.text}"
