from pyAudioAnalysis import audioTrainTest as aT


class ML:

    def train_model(self, *args, path_to_save=''):
        aT.extract_features_and_train(args, 1.0, 1.0, aT.shortTermWindow,
                                      aT.shortTermStep, "svm", path_to_save, True)

    def classify(self, file_path, model_path):
        result = aT.file_classification(file_path, model_path, "svm")
        return result[0] == 0 and result[1][0] > 0.9
