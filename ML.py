from functools import partial
from multiprocessing import Pool

import librosa
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from joblib import dump, load


class ML:

    def extract_features(self, file_name):
        try:
            print(f"Extracting audio features from {file_name[0]}...")
            audio, sample_rate = librosa.load(file_name[0], sr=None, res_type='kaiser_fast')
            zcr = librosa.feature.zero_crossing_rate(y=audio)
            spectral_centroid = librosa.feature.spectral_centroid(y=audio)
            spectral_contrast = librosa.feature.spectral_contrast(y=audio)
            spectral_bandwith = librosa.feature.spectral_bandwidth(y=audio)
            spectral_rolloff = librosa.feature.spectral_rolloff(y=audio)
            mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate)

            return [[np.mean(zcr), np.std(zcr), np.mean(spectral_centroid), np.std(spectral_centroid),
                     np.mean(spectral_contrast), np.std(spectral_contrast), np.mean(spectral_bandwith),
                     np.std(spectral_bandwith), np.mean(spectral_rolloff), np.std(spectral_rolloff),
                     np.mean(mfccs[1, :]), np.std(mfccs[1, :]), np.mean(mfccs[2, :]), np.std(mfccs[2, :]),
                     np.mean(mfccs[3, :]), np.std(mfccs[3, :]), np.mean(mfccs[4, :]), np.std(mfccs[4, :]),
                     np.mean(mfccs[5, :]), np.std(mfccs[5, :]), np.mean(mfccs[6, :]), np.std(mfccs[6, :]),
                     np.mean(mfccs[7, :]), np.std(mfccs[7, :]), np.mean(mfccs[8, :]), np.std(mfccs[8, :]),
                     np.mean(mfccs[9, :]), np.std(mfccs[9, :]), np.mean(mfccs[10, :]), np.std(mfccs[10, :]),
                     np.mean(mfccs[11, :]), np.std(mfccs[11, :]), np.mean(mfccs[12, :]), np.std(mfccs[12, :]),
                     np.mean(mfccs[13, :]), np.std(mfccs[13, :])], file_name[1]]
        except Exception as e:
            print(e)

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

        with Pool(4) as p:
            results = p.map(self.extract_features, file_names)
        for result in results:
            features.append(result[0])
            target.append(result[1])
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
        result = self.extract_features([file_path, term])
        if result is not None:
            prediction = model.predict_proba([result[0]])[0][0]
            if prediction > 0.95:
                return file_path.split('/')[-1].split('.')[0]
            else:
                return None

