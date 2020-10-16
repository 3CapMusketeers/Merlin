import shutil

from app.ML import ML
from app.SpotifyAPI import SpotifyAPI
import os

from app.utils.file_utils import write_file
from multiprocessing import Pool


class ModelHandler:

    def __init__(self):
        self.spotify_api = SpotifyAPI()
        self.ml = ML()

    def _write_mp3s(self, track_dict):
        content = self.spotify_api.get_mp3(track_dict['url'])
        if content:
            write_file(f'{track_dict["id"]}.mp3', content)

    def write_mp3s(self, tracks_dict):
        with Pool(4) as p:
            p.map(self._write_mp3s, tracks_dict)

    def create_model(self, uid, tracks_dict):
        if uid not in os.listdir():
            os.mkdir(uid)
            os.mkdir(f"{uid}/liked")
            os.chdir(f"{uid}/liked")
            self.write_mp3s(tracks_dict)
            os.chdir("../..")
            self.ml.train_model(f"{uid}/liked", path_to_save=f"{uid}/model", uid=uid)

    def classify_tracks(self, training_tracks, tracks_to_classify, search_term, uid):
        if uid not in os.listdir():
            return None
        if search_term not in os.listdir():
            os.mkdir(search_term)
            os.chdir(search_term)
            self.write_mp3s(training_tracks)
            os.chdir('../../appi')
            self.ml.train_model(f"{search_term}", path_to_save=f"{search_term}/model")
            file_paths = []
            for track_to_classify in tracks_to_classify:
                file_paths.append(f"{uid}/liked/{track_to_classify['id']}.mp3")
            track_ids = self.ml.classify_tracks(file_paths, f"{search_term}/model", search_term)
        else:
            file_paths = []
            for track_to_classify in tracks_to_classify:
                file_paths.append(f"{uid}/liked/{track_to_classify['id']}.mp3")
            track_ids = self.ml.classify_tracks(file_paths, f"{search_term}/model", search_term)
        return track_ids

    def curated_tracks(self, tracks_to_classify, uid):
        if f"{uid}" not in os.listdir() or "model" not in os.listdir(f"{uid}"):
            return None
        os.mkdir(f'{uid}/tmp')
        os.chdir(f"{uid}/tmp")
        self.write_mp3s(tracks_to_classify)
        os.chdir('../..')
        file_paths = []
        for track_to_classify in tracks_to_classify:
            file_paths.append(f"{uid}/tmp/{track_to_classify['id']}.mp3")
        track_ids = self.ml.classify_tracks(file_paths, f"{uid}/model", "liked")
        shutil.rmtree(f'{uid}/tmp')
        return track_ids

    def check_personal_model(self, user_id):
        files = os.listdir()
        return user_id in files and 'model' in os.listdir(user_id)
