from flask import request


def required_login():
    ctx = request.authorization
    print(ctx)