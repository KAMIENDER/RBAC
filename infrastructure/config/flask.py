from flask.app import Flask

app = Flask(__name__)
app.config.from_pyfile('dev_config.py')
