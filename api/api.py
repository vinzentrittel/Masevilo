import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Trash Map</h1><p>This is going to be our trash map</p>"

app.run()
