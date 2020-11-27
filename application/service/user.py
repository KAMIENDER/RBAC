import logging

from flask import request
from flask_restful import Resource

from application.request.user import UserRegisterRequestModel
from domains.user.service.facade import create_user


class UserReource(Resource):
    def post(self):
        args = request.get_json()
        args = UserRegisterRequestModel.parse_obj(args)
        logging.debug(args.name)
        create_user(args)
        return {
            'message': 'ok'
        }
