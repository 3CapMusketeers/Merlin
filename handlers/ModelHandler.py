from SpotifyAPI import SpotifyAPI
import os
from pyAudioAnalysis import audioTrainTest as aT


class ModelHandler:

    def __init__(self):
        self.spotify_api = SpotifyAPI()

    def create_model(self, uid, tracks_dict):
        tracks = []
        for track in tracks_dict:
            tracks.append([track['url'], track['id']])
        if uid not in os.listdir():
            os.mkdir(uid)
            os.mkdir(f"{uid}/liked")
            for track in tracks:
                with open(f"{uid}/liked/{track[1]}.mp3", "wb") as file:
                    file.write(self.spotify_api.get_mp3(track[0]))
            aT.extract_features_and_train([f"{uid}/liked", "../random music"], 1.0, 1.0, aT.shortTermWindow,
                                          aT.shortTermStep, "svm", f"{uid}/svmSMtemp", True)
            
