

from infrastructure.config.blueprint import register
from infrastructure.config.flask import app

if __name__ == '__main__':
    register(app)
    app.run(debug=True)