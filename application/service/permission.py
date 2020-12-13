import logging

from flask import request
from flask_restful import Resource
from pydantic import BaseModel

from domains.permission.service.permission_facade import *
from infrastructure.config.before_request import RBACResource


class PermissionModel(BaseModel):
    id: int
    disable: int
    key: str
    name: str
    level: str
    extra: str = None

    class Config:
        orm_mode = True


class PermissionBasicResource(Resource):
    #  新建权限
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

    # 查找权限
    def get(self):
        args = request.args
        try:
            owner_keys = args.getlist("owner_keys", type=str)
            permission_keys = args.getlist('permission_keys', type=str) or []
            permission_name = args.get('permission_name', type=str, default='')
            permission_level = args.get('permission_level', type=int)
            disable = args.get('permission_disable', type=int)
            if disable:
                disable = PermissionDisable(disable)
        except Exception as e:
            return {
                       'message': 'args error'
                   }, 400
        try:
            out = list()
            if owner_keys:
                owner_permissions = get_permissions_users_ownerd(user_keys=owner_keys, disable=disable)
                permission_keys.extend([permission.key for permission in owner_permissions])
            permissions = get_permissions(
                keys=permission_keys, name=permission_name, level=permission_level, disable=disable)
            for permission in permissions:
                out.append(dict(PermissionModel.from_orm(permission)))
        except Exception as e:
            logging.error(f'search permission error: {e}')
            return {
                'messgae': 'some thing error'
            }, 500
        return {'data': out}, 200


class PermissionAuthResource(RBACResource):
    # 查询用户拥有的权限
    def get(self):
        args = request.args
        try:
            user_keys = args.getlist("user_keys", type=str)
            permission_keys = args.getlist('permission_keys', type=str) or []
            permission_name = args.get('permission_name', type=str, default='')
            permission_level = args.get('permission_level', type=int)
            disable = args.get('permission_disable', type=int)
            out = list()
            if user_keys:
                had_permissions = get_permissions_users_had(user_keys=user_keys, disable=disable)
                permission_keys.extend([permission.key for permission in had_permissions])
                owner_permissions = get_permissions_users_ownerd(user_keys=user_keys, disable=disable)
                permission_keys.extend([permission.key for permission in owner_permissions])
            permissions = get_permissions(
                keys=permission_keys, name=permission_name, level=permission_level, disable=disable)
            for permission in permissions:
                out.append(dict(PermissionModel.from_orm(permission)))
        except Exception as e:
            logging.error(f"permission auth api error: {e}")
            return {
                       'messgae': 'some thing error'
                   }, 500
        return {'data': out}, 200

    # 给用户、角色授权
    def post(self):
        args = request.get_json()
        owner_key = request.authorization.username
        permission_keys = args.get("permission_keys") or list()
        temp = judge_permissions_items_owned(permission_keys, [owner_key], ItemType.user)
        test = temp[owner_key]
        if len(test) != len(permission_keys):
            return {
                'message': 'you are not some permissions owner'
            }, 403
        user_keys = args.get("user_keys") or list()
        role_keys = args.get("role_keys") or list()
        if user_keys:
            result = grant_permissions_to_items(
                permission_keys=permission_keys, item_keys=user_keys, item_type=ItemType.user)
            if not result:
                return {
                    'message': "grant permissions to users error"
                }, 500

        if role_keys:
            result = grant_permissions_to_items(
                permission_keys=permission_keys, item_keys=role_keys, item_type=ItemType.role)
            if not result:
                return {
                       'message': "grant permissions to roles error"
                   }, 500
        return {
            'message': 'ok'
        }, 200

