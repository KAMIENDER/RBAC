from infrastructure.config.before_request import required_login
from infrastructure.config.blueprint import register
from infrastructure.config.flask import app

if __name__ == '__main__':
    register(app)
    app.before_request(required_login)
    app.run(debug=True)