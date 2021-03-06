import shutil
from functools import partial

from ML import ML
from SpotifyAPI import SpotifyAPI
import os

from utils.file_utils import write_file
from multiprocessing import Pool


class ModelHandler:

    def __init__(self):
        self.spotify_api = SpotifyAPI()
        self.ml = ML()

    def _write_mp3s(self, path, track_dict):
        content = self.spotify_api.get_mp3(track_dict['url'])
        if content:
            write_file(f'{path}/{track_dict["id"]}.mp3', content)

    def write_mp3s(self, tracks_dict, path):
        func = partial(self._write_mp3s, path)
        with Pool(4) as p:
            p.map(func, tracks_dict)

    def create_model(self, uid, tracks_dict):
        if uid not in os.listdir():
            os.mkdir(uid)
            os.mkdir(f"{uid}/liked")
            self.write_mp3s(tracks_dict, f"{uid}/liked")
            self.ml.train_model(f"{uid}/liked", path_to_save=f"{uid}/model", uid=uid)

    def classify_tracks(self, training_tracks, tracks_to_classify, search_term, uid):
        if uid not in os.listdir():
            return None
        if search_term not in os.listdir():
            os.mkdir(search_term)
            self.write_mp3s(training_tracks, f"{search_term}")
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
        self.write_mp3s(tracks_to_classify, f"{uid}/tmp")
        file_paths = []
        for track_to_classify in tracks_to_classify:
            file_paths.append(f"{uid}/tmp/{track_to_classify['id']}.mp3")
        track_ids = self.ml.classify_tracks(file_paths, f"{uid}/model", "liked")
        shutil.rmtree(f'{uid}/tmp')
        return track_ids

    def check_personal_model(self, user_id):
        files = os.listdir()
        if user_id in files and 'model' in os.listdir(user_id):
            return 1
        elif user_id in files and 'model' not in os.listdir(user_id):
            return 0
        else:
            return -1


