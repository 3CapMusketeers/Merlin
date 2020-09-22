from functools import partial
from multiprocessing import Pool

import librosa
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from joblib import dump, load


class ML:

    def extract_features(self, file_names):
        results = []
        for file_name in file_names:
            try:
                print(f"Extracting audio features from {file_name}...")
                audio, sample_rate = librosa.load(file_name[0])
                mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
                mfccsscaled = np.mean(mfccs.T, axis=0)
                results.append([mfccsscaled, file_name[1]])
            except Exception as e:
                print(e)
        return results

    def split_list(self, mylist, chunk_size):
        return [mylist[offs:offs + chunk_size] for offs in range(0, len(mylist), chunk_size)]

    def train_model(self, *args, path_to_save='', uid=''):
        features = []
        target = []
        file_names = []
        for directory in args:
            files = os.listdir(directory)
            directory = directory.split('/')[-1]
            for file in files:
                if file.split('.')[1] == "mp3":
                    if uid:
                        file_path = os.getcwd() + '/' + uid + '/' + directory + '/' + file
                    else:
                        file_path = os.getcwd() + '/' + directory + '/' + file
                    file_names.append([file_path, directory])

        file_names = self.split_list(file_names, 100)

        with Pool(4) as p:
            results = p.map(self.extract_features, file_names)
        for result in results:
            for file_name in result:
                features.append(file_name[0])
                target.append(file_name[1])
        with open("random music/random music.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                features.append(np.fromstring(line, sep=","))
                target.append("random music")

        x_train, x_test, y_train, y_test = train_test_split(features, target)
        clf = RandomForestClassifier()
        print("training...")
        model = clf.fit(x_train, y_train)
        print('accuracy train: %f' % model.score(x_train, y_train))
        print('accuracy on test: %f' % model.score(x_test, y_test))

        dump(model, path_to_save)

    def classify_tracks(self, file_paths, model_path, term):
        func = partial(self.classify, model_path, term)
        with Pool(4) as p:
            results = p.map(func, file_paths)
        track_ids = list(filter(None, results))
        return track_ids

    def classify(self, model_path, term, file_path):
        model = load(model_path)
        if model.predict([self.extract_features(file_path)]) == term:
            return file_path.split('/')[-1].split('.')[0]
        else:
            return None

