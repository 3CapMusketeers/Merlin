import os
import json
import requests


class SpotifyAPI:

    token = ''

    def __init__(self):
        self.base_url = "https://api.spotify.com/v1"

    def request_data(self, url, token=token, method='GET', body=None):
        header = {'Authorization': 'Bearer ' + token} if token else None
        if method == 'GET':
            response = requests.get(self.base_url + url, headers=header)
        else:
            response = requests.post(self.base_url + url, headers=header, json=body)
        return json.loads(response.text) if response.text else None

    def get_mp3(self, url):
        print(f"Getting {url}...")
        return requests.get(url).content

    def set_token(self, token):
        self.token = token




