import flask

STATICS = "web"
app = flask.Flask(__name__, root_path=".", static_folder=STATICS)


@app.route('/', methods=["GET"])
def root():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)
