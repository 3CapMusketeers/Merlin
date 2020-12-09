import unittest
import os

from ML import ML


class MLTestCase(unittest.TestCase):

    def test_train_model(self):
        ml = ML()
        ml.train_model("test_music", "test_music_2", path_to_save="tester_model")
        assert "tester_model" in os.listdir()

    def test_classify_tracks(self):
        ml = ML()
        ml.classify_tracks(['test_music/514q3otlT6HczfChuLDUSa.mp3'], "tester_model", "test_music")


if __name__ == '__main__':
    unittest.main()
