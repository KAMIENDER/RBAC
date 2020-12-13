import functools
import logging

from flask import request, jsonify

from flask_restful import Resource
from domains.user.service.facade import get_users


def required_login():
    if request.endpoint == 'userresource':
        return
    ctx = request.authorization
    if not ctx:
        return {'message': 'no auth'}, 403
    users = get_users(keys=[ctx.username])
    if not users or users[0].password != ctx.password:
        return {'message': 'username or password error'}, 403
    logging.debug(f"user {ctx.username} visit")
    return


def catch_exception(func):

    @functools.wraps(func)
    def _func(*args, **kws):
        # noinspection PyBroadException
        try:
            return func(*args, **kws)
        except Exception as e:
            logging.error(f"request error: {request.path}, error: {e}")
            return jsonify(message="系统内部错误, 请联系管理员。"), 500

    return _func


class RBACResource(Resource):
    # method_decorators = [catch_exception]
    pass