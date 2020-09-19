from ML import ML
from SpotifyAPI import SpotifyAPI
import os


class ModelHandler:

    def __init__(self):
        self.spotify_api = SpotifyAPI()
        self.ml = ML()

    def create_model(self, uid, tracks_dict):
        if uid not in os.listdir():
            os.mkdir(uid)
            os.mkdir(f"{uid}/liked")
            for track in tracks_dict:
                with open(f"{uid}/liked/{track['id']}.mp3", "wb") as file:
                    file.write(self.spotify_api.get_mp3(track['url']))
            self.ml.train_model(f"{uid}/liked", "random music", path_to_save=f"{uid}/model")

    def classify_tracks(self, training_tracks, tracks_to_classify, search_term, uid):
        if search_term not in os.listdir():
            os.mkdir(search_term)
            if uid not in os.listdir():
                os.mkdir(uid)
            for count, training_track in enumerate(training_tracks):
                with open(f"{search_term}/{count}.mp3", "wb") as file:
                    file.write(self.spotify_api.get_mp3(training_track['url']))
            for track_to_classify in tracks_to_classify:
                with open(f"{uid}/liked/{track_to_classify['id']}.mp3", "wb") as file:
                    file.write(self.spotify_api.get_mp3(track_to_classify['url']))
            self.ml.train_model(f"{search_term}", "random music", path_to_save=f"{search_term}/model")

            track_ids = []
            for track_to_classify in tracks_to_classify:
                result = self.ml.classify(f'{uid}/liked/{track_to_classify["id"]}.mp3', f'{search_term}/model')
                if result:
                    track_ids.append(track_to_classify['id'])
            return track_ids
        else:
            pass
