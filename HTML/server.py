from flask import Flask, request, render_template
from flask.helpers import send_from_directory
from predictor.predictor import predict_personality

app = Flask(__name__)


@app.route('/')  # the site to route to, index/main in this case
def hello_world():
    return send_from_directory('.', 'index.html')


@app.route('/favicon.ico')  # the site to route to, index/main in this case
def send_favicon():
    return send_from_directory('./', 'favicon.ico')


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)


@app.route('/pages/<path:path>')
def send_pages(path):
    return send_from_directory('pages', path)


@app.route('/media/<path:path>')
def send_media(path):
    return send_from_directory('media', path)


@app.route('/getprediction')
def get_prediction():
    return predict_personality(request.args.to_dict()['content'])


# This just gets flask running
app.run(port=5000, debug=True)
