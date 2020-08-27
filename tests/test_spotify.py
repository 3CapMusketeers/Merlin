import unittest
from SpotifyAPI import SpotifyAPI
import os


class SpotifyAPITestCase(unittest.TestCase):
    def setUp(self):
        os.environ['SPOT_URL'] = 'https://5f47d89495646700168da0a0.mockapi.io/'

    def test_request_data(self):
        spotify_api = SpotifyAPI()
        name = spotify_api.request_data('test')[0]['name']
        self.assertEqual(name, 'ok')
        post_name = spotify_api.request_data('test', method='POST')[0]['post']
        self.assertEqual(post_name, "ok")

    def test_set_token(self):
        spotify_api = SpotifyAPI()
        spotify_api.set_token("token")
        self.assertEqual(spotify_api.token, "token")

    def test_get_mp3(self):
        spotify_api = SpotifyAPI()
        spotify_api.get_mp3('https://p.scdn.co/mp3-preview/4839b070015ab7d6de9fec1756e1f3096d908fba?cid=774b29d4f13844c495f206cafdad9c86')



if __name__ == '__main__':
    unittest.main()
