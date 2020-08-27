import unittest
import os
import shutil

from handlers.ModelHandler import ModelHandler


class ModelHandlerTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['SPOT_URL'] = 'https://5f47d89495646700168da0a0.mockapi.io/'

    def tearDown(self):
        shutil.rmtree("1")

    def test_create_model(self):
        tracks_dict = [
            {"url": "https://p.scdn.co/mp3-preview/104ad0ea32356b9f3b2e95a8610f504c90b0026b?cid=774b29d4f13844c495f206cafdad9c86",
             "id": "4VqPOruhp5EdPBeR92t6lQ"},
            {"url": "https://p.scdn.co/mp3-preview/b326e03624cb098d8387e17aa46669edac0d025a?cid=774b29d4f13844c495f206cafdad9c86",
             "id": "2takcwOaAZWiXQijPHIx7B"}
        ]

        ModelHandler().create_model('1', tracks_dict)
        assert "1" in os.listdir()
        assert "liked" in os.listdir(os.getcwd() + "/1")
        assert "svmSMtemp" in os.listdir(os.getcwd() + "/1")



if __name__ == '__main__':
    unittest.main()