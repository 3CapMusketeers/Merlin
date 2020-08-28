from flask import Flask, request, jsonify

from handlers.ModelHandler import ModelHandler

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/model', methods=['POST'])
def create_model():
    uid = request.json['uid']
    track_urls = request.json['tracks']
    ModelHandler().create_model(uid, track_urls)
    return jsonify(msg="ok")


if __name__ == '__main__':
    app.run()
