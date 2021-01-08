from infrastructure.config.redis import redis_client
from wsgi import app

if __name__ == '__main__':
    redis_client.hmset('test', {1:2})
    app.run(debug=True)