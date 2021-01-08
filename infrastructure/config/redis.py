import redis

from infrastructure.config.flask import app

redis_client = redis.from_url(app.config.get('REDIS_URL'))