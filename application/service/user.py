import logging

from flask import request, jsonify
from flask_restful import Resource
from pydantic.main import BaseModel

from application.request.user import UserRegisterRequestModel
from domains.user.entity.value import UserType
from domains.user.service.facade import create_user, get_users, update_user


class UserResource(Resource):
    class UserModel(BaseModel):
        key: str
        name: str
        email: str = None
        phone: str = None
        extra: str = None
        type: int
        level: int

        class Config:
            orm_mode = True

    def post(self):
        try:
            args = request.get_json()
            args = UserRegisterRequestModel.parse_obj(args)
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
        out = list()
        for user in users:
            out.append(dict(self.UserModel.from_orm(user)))
        return {
            'data': out
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
