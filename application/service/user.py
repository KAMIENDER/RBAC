import logging

from flask import request
from flask.views import MethodView

from application.request.user import UserRegisterRequestModel


class UserReource(MethodView):
    def post(self):
        args = request.args
        args = UserRegisterRequestModel(args)
        logging.debug(args.name)
        return {
            'message': 'ok'
        }
