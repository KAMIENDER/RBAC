import json
import logging

import redis
import gunicorn

from infrastructure.config.flask import app


class RBACRedis:
    __redis_client = redis.from_url(app.config.get('REDIS_URL'))

    @classmethod
    def set_hash(cls, name: str, key: str, value):
        try:
            cls.__redis_client.hset(name, key, json.dumps(value))
        except Exception as e:
            logging.error(f'redis set hash error: {e}')
            return False
        return True

    @classmethod
    def get_hash(cls, name: str, key: str):
        temp = cls.__redis_client.hget(name, key)
        if temp:
            return json.loads(temp)
        return None

    @classmethod
    def set_str(cls, name: str, value):
        try:
            cls.__redis_client.set(name, json.dumps(value))
        except Exception as e:
            logging.error(f'redis set hash error: {e}')
            return False
        return True

    @classmethod
    def get_str(cls, name: str):
        temp = cls.__redis_client.get(name)
        if temp:
            return json.loads(temp)
        return None
