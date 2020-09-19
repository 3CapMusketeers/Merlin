import unittest
import os
import shutil

from handlers.ModelHandler import ModelHandler


class ModelHandlerTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['SPOT_URL'] = 'https://5f47d89495646700168da0a0.mockapi.io/'

    def test_create_model(self):
        os.chdir("../")
        tracks_dict = [
            {"url": "https://p.scdn.co/mp3-preview/104ad0ea32356b9f3b2e95a8610f504c90b0026b?cid=774b29d4f13844c495f206cafdad9c86",
             "id": "4VqPOruhp5EdPBeR92t6lQ"},
            {"url": "https://p.scdn.co/mp3-preview/b326e03624cb098d8387e17aa46669edac0d025a?cid=774b29d4f13844c495f206cafdad9c86",
             "id": "2takcwOaAZWiXQijPHIx7B"}
        ]

        ModelHandler().create_model(os.getcwd() + "/tests/1", tracks_dict)
        assert "1" in os.listdir(os.getcwd() + "/tests")
        assert "liked" in os.listdir(os.getcwd() + "/tests/1")
        assert "model" in os.listdir(os.getcwd() + "/tests/1")
        shutil.rmtree(os.getcwd() + "/tests/1")

    def test_classify_tracks(self):
        training_tracks = [
            {'url': "https://p.scdn.co/mp3-preview/104ad0ea32356b9f3b2e95a8610f504c90b0026b?cid=774b29d4f13844c495f206cafdad9c86"}
        ]
        tracks_to_classify = [
            {'url': "https://p.scdn.co/mp3-preview/b326e03624cb098d8387e17aa46669edac0d025a?cid=774b29d4f13844c495f206cafdad9c86",
             "id": "2takcwOaAZWiXQijPHIx7B"}
        ]
        search_term = 'test'
        ModelHandler().classify_tracks(training_tracks, tracks_to_classify, search_term, "1")


if __name__ == '__main__':
    unittest.main()
