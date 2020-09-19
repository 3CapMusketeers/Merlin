from flask import Flask, request, jsonify

from handlers.ModelHandler import ModelHandler

app = Flask(__name__)


@app.route('/model', methods=['POST'])
def create_model():
    uid = request.json['uid']
    track_urls = request.json['tracks']
    ModelHandler().create_model(uid, track_urls)
    return jsonify(msg="ok")


@app.route('/classifier', methods=['POST'])
def classify_tracks():
    training_tracks = request.json['training_tracks']
    tracks_to_classify = request.json['classify_tracks']
    search_term = request.json['search_term']
    uid = request.json['uid']
    ModelHandler().classify_tracks(training_tracks, tracks_to_classify, search_term, uid)


if __name__ == '__main__':
    app.run()
