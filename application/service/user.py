import logging

from flask import request
from flask_restful import Resource

from application.request.user import UserRegisterRequestModel
from domains.user.entity.value import UserType
from domains.user.service.facade import create_user, get_users, update_user


class UserResource(Resource):
    def post(self):
        try:
            args = request.get_json()
            args = UserRegisterRequestModel.parse_obj(args)
            logging.debug(args.name)
            create_user(args)
        except Exception as e:
            logging.error(f"user resource create user error: {e}, args: {args}")
            return {
                'message': 'error'
            }
        return {
            'message': 'ok'
        }

    def get(self):
        keys = request.args.getlist('keys', type=str)
        name = request.args.get('name', default='', type=str)
        level = request.args.get('level', default=0, type=int)
        user_type = request.args.get('type', type=int)
        if user_type:
            user_type = UserType(user_type)
        if not level:
            level = 0
        phones = request.args.getlist('phones', type=int) or None
        email = request.args.get('email', type=str, default='') or None
        users = get_users(keys=keys, name=name, user_type=user_type, phones=phones, email=email, level=level)
        return {
            'data': users
        }


class UserUpdateResource(Resource):
    def post(self):
        args = request.get_json()
        keys = args.get("keys")
        users = get_users(keys=keys)
        if not users:
            return {
                "message": "Not user"
            }
        name = args.get("name")
        level = args.get('level', None)
        type = args.get('type', None)
        password = args.get('password', None)
        if type:
            type = UserType(type)
        phone = args.get('phone', None)
        email = args.get('email', None)
        for user in users:
            if not update_user(user, name=name, level=level, type=type, phone=phone, email=email, password=password):
                return {
                    'message': 'error'
                }
        return {
            'message': 'ok'
        }
