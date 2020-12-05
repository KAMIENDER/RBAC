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
        keys = request.args.getlist('keys', str) or None
        name = request.args.get('name', str) or None
        level = request.args.get('level', int) or None
        type = request.args.get('type') or None
        if type:
            type = UserType(type)
        phones = request.args.getlist('phones', int) or None
        email = request.args.get('email', str) or None
        users = get_users(keys, name=name, level=level, user_type=type, phones=phones, email=email)
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
