import unittest
import os
import shutil

from handlers.ModelHandler import ModelHandler
from pyAudioAnalysis import audioTrainTest as aT


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
        os.chdir("../")
        training_tracks = [
            {'url': "https://p.scdn.co/mp3-preview/104ad0ea32356b9f3b2e95a8610f504c90b0026b?cid=774b29d4f13844c495f206cafdad9c86"},
            {'url': "https://p.scdn.co/mp3-preview/b326e03624cb098d8387e17aa46669edac0d025a?cid=774b29d4f13844c495f206cafdad9c86"}
        ]
        tracks_to_classify = [
            {'url': "https://p.scdn.co/mp3-preview/b326e03624cb098d8387e17aa46669edac0d025a?cid=774b29d4f13844c495f206cafdad9c86",
             "id": "2takcwOaAZWiXQijPHIx7B"}
        ]
        search_term = 'test'
        ModelHandler().classify_tracks(training_tracks, tracks_to_classify, search_term, "1")
        ModelHandler().classify_tracks(training_tracks, tracks_to_classify, search_term, "1")
        shutil.rmtree("1")
        shutil.rmtree("test")

    def test_curated_playlist(self):
        os.mkdir("1")
        tracks_to_classify = [
            {
                'url': "https://p.scdn.co/mp3-preview/b326e03624cb098d8387e17aa46669edac0d025a?cid=774b29d4f13844c495f206cafdad9c86",
                "id": "2takcwOaAZWiXQijPHIx7B"}
        ]
        tracks_ids = ModelHandler().curated_tracks(tracks_to_classify, "1")
        assert tracks_ids is None
        aT.extract_features_and_train(["test_music", "test_music_2"], 1.0, 1.0, aT.shortTermWindow,
                                      aT.shortTermStep, "svm", "1/model", True)
        track_ids = ModelHandler().curated_tracks(tracks_to_classify, "1")
        assert isinstance(track_ids, list)
        shutil.rmtree("1")


if __name__ == '__main__':
    unittest.main()
