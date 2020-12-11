import logging

from flask import request
from flask_restful import Resource
from pydantic import BaseModel

from domains.permission.service.permission_facade import create_permission, get_user_owned_permissions, \
    get_user_had_but_not_owned_permissions


class PermissionBasicResource(Resource):
    class PermissionModel(BaseModel):
        id: int
        disable: int
        key: str
        name: str
        level: str
        extra: str = None

        class Config:
            orm_mode = True

    def post(self):
        args = request.get_json()
        try:
            owner_keys = args.get('owner_keys') or None
            permission_key = args.get('permission_key') or None
            permission_name = args.get('permission_name') or None
            permission_level = args.get('permission_level') or None
            if not all([owner_keys, permission_key, permission_name, permission_level]):
                return {
                    'message': 'need more args'
                }, 400
        except Exception:
            return {
                'message': 'args error'
            }, 400
        if create_permission(
                owner_keys=owner_keys, permission_key=permission_key,
                permission_name=permission_name, permission_level=permission_level):
            return {
                'message': 'ok'
            }, 200
        return {
            'message': 'create failed'
        }

    def get(self):
        args = request.args
        try:
            owner_key = request.authorization.username
            permission_keys = args.getlist('permission_keys', type=str)
            permission_name = args.get('permission_name', type=str, default='')
            permission_level = args.get('permission_level', type=int)
        except Exception as e:
            return {
                       'message': 'args error'
                   }, 400
        try:
            permissions = get_user_owned_permissions(
                owner_keys=[owner_key], permission_level=permission_level, permission_name=permission_name,
                permission_keys=permission_keys)
            permissions_had = get_user_had_but_not_owned_permissions(
                user_keys=[owner_key], permission_level=permission_level, permission_name=permission_name,
                permission_keys=permission_keys)
            permissions.extend(permissions_had)
            out = list()
            in_out_permission_keys = list()
            for permission in permissions:
                if permission.key in in_out_permission_keys:
                    continue
                out.append(dict(self.PermissionModel.from_orm(permission)))
                in_out_permission_keys.append(permission.key)
        except Exception as e:
            logging.error(f'{owner_key} get permission error: {e}')
            return {
                'messgae': 'some thing error'
            }, 500
        return {'data': out}, 200


class PermissionAuthResource(Resource):
    def get(self):
        try:
            args = request.args
            user_keys = args.getlist(key='user_keys')
            role_keys = args.getlist(key='role_keys')
            permission_keys = args.getlist(key='permission_keys')
            if not any([user_keys, role_keys]) or not permission_keys:
                return {'message': 'need more args'}, 400
        except Exception as e:
            return {
                   'message': 'args error'
               }, 400
        try:
            out = dict()
            for user_key in user_keys:
                permissions = get_user_owned_permissions(
                    owner_keys=[user_key], permission_keys=permission_keys)
                permissions_had = get_user_had_but_not_owned_permissions(
                    user_keys=[user_key], permission_keys=permission_keys)

        except Exception as e:
            logging.error(f'{request.authorization.username} auth error: {e}')
            return {
                'message': 'internale error'
            }, 500

