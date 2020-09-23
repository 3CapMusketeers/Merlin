import os
import json
import requests


class SpotifyAPI:

    token = ''

    def __init__(self):
        self.base_url = "https://api.spotify.com/v1"

    def get_mp3(self, url):
        print(f"Getting {url}...")
        return requests.get(url).content

    def set_token(self, token):
        self.token = token




