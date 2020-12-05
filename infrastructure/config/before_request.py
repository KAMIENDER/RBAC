import logging

from flask import request

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