import logging

from flask import request, jsonify
from flask_restful import Resource

from domains.permission.service.permission_facade import *


class PermissionBasicResource(Resource):
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
            permissions = get_permissions(
                owner_keys=[owner_key], permission_level=permission_level, permission_name=permission_name,
                permission_keys=permission_keys)
        except Exception as e:
            logging.error(f'{owner_key} get permission error: {e}')
            return {
                'messgae': 'some thing error'
            }, 500
        return jsonify(permissions), 200
