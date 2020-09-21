from pyAudioAnalysis import audioTrainTest as aT
import librosa
import numpy as np
import os
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from joblib import dump, load


class ML:

    def extract_features(self, file_name):
        try:
            audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast')
            mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
            mfccsscaled = np.mean(mfccs.T, axis=0)

        except Exception as e:
            return None
        return mfccsscaled

    def train_model(self, *args, path_to_save='', uid=''):
        features = []
        target = []
        for directory in args:
            files = os.listdir(directory)
            directory = directory.split('/')[-1]
            for file in files:
                if file.split('.')[1] == "mp3":
                    if uid:
                        file_path = os.getcwd() + '/' + uid + '/' + directory + '/' + file
                    else:
                        file_path = os.getcwd() + '/' + directory + '/' + file
                    features.append(self.extract_features(file_path))
                    target.append(directory)
        x_train, x_test, y_train, y_test = train_test_split(features, target)
        clf = RandomForestClassifier()
        model = clf.fit(x_train, y_train)
        print('accuracy train: %f' % model.score(x_train, y_train))
        print('accuracy on test: %f' % model.score(x_test, y_test))

        dump(model, path_to_save)

    def classify(self, file_path, model_path, term):
        model = load(model_path)
        return model.predict([self.extract_features(file_path)]) == term

