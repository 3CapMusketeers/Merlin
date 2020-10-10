import datetime

from flask import Flask, request, jsonify

from handlers.ModelHandler import ModelHandler

app = Flask(__name__)


@app.route('/personal-models', methods=['POST'])
def create_model():
    current_time = datetime.datetime.now()
    uid = request.json['uid']
    track_urls = request.json['tracks']
    ModelHandler().create_model(uid, track_urls)
    passed_time = datetime.datetime.now()
    print(passed_time - current_time)
    return jsonify(msg="ok")


@app.route('/classifier', methods=['POST'])
def classify_tracks():
    training_tracks = request.json['training_tracks']
    tracks_to_classify = request.json['classify_tracks']
    search_term = request.json['search_term']
    uid = request.json['uid']
    track_ids = ModelHandler().classify_tracks(training_tracks, tracks_to_classify, search_term, uid)
    if track_ids is None:
        return jsonify(msg="User must create an account first")
    else:
        return jsonify(tracks=track_ids)


@app.route('/personal-models/<user_id>/classification', methods=['POST'])
def curated_playlist(user_id):
    tracks_to_classify = request.json['classify_tracks']
    track_ids = ModelHandler().curated_tracks(tracks_to_classify, user_id)
    if track_ids is None:
        return jsonify(msg="Personal Model not yet created")
    return jsonify(tracks=track_ids)


if __name__ == '__main__':
    app.run(port=5005)
