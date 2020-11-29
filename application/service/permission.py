import logging
from importlib.resources import Resource

from flask import request

from domains.permission.service.permission_facade import create_permission


class PermissionBasicResource(Resource):
    def post(self):
        args = request.get_json()
        try:
            owner_keys = args.get('owner_keys')
            permission_key = args.get('permission_key')
            permission_name = args.get('permission_name')
            permission_level = args.get('permission_level')
        except Exception:
            return {
                'message': 'args error'
            }
        if create_permission(
                owner_keys=owner_keys, permission_key=permission_key,
                permission_name=permission_name, permission_level=permission_level):
            return {
                'message': 'ok'
            }
        return {
            'message': 'create failed'
        }

