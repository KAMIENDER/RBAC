from flask import Flask

from infrastructure.config.before_request import required_login

app = Flask(__name__)
app.before_request(required_login)
