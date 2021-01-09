import logging
from typing import List

from flask import request
from flask_restful import Resource
from pydantic.main import BaseModel

from domains.item.entity.const import ItemRefDisable
from domains.role.entity.value import RoleType
from domains.role.service.role_facade import create_role, get_roles, update_role
import domains.role.service.role_facade as role_facade
from infrastructure.config.before_request import RBACResource
import domains.item.service.item_facade as item_facade


class RoleResource(Resource):
    class RoleModel(BaseModel):
        owner_keys: List[str]
        key: str
        name: str
        extra: str = None
        type: int
        level: int

        class Config:
            orm_mode = True

    def post(self):
        try:
            args = request.get_json()
            args = self.RoleModel.parse_obj(args)
            if not create_role(args):
                return {
                    'message': 'something error, please check params'
                }
        except Exception as e:
            logging.error(f"role resource create role error: {e}, args: {args}")
            return {
                'message': 'get args error'
            }
        return {
            'message': 'ok'
        }

    def get(self):
        keys = request.args.getlist('keys', type=str)
        name = request.args.get('name', default='', type=str)
        level = request.args.get('level', default=0, type=int)
        role_type = request.args.get('type', type=int)
        if role_type:
            role_type = RoleType(role_type)
        if not level:
            level = 0
        roles = get_roles(keys=keys, name=name, role_type=role_type, level=level)
        out = list()
        for role in roles:
            out.append({
                'name': role.name,
                'extra': role.extra,
                'id': role.id,
                'key': role.key,
                'level': role.level,
            })
        return {
            'data': out
        }

    def delete(self):
        keys = request.args.getlist('keys', type=str)
        if not keys:
            return {
                'msg': 'missing params keys'
            }, 400
        roles = role_facade.get_roles(keys=keys)
        if role_facade.delete_roles(roles):
            return {
                'msg': 'ok'
            }, 200
        return {
            'msg': 'fail to delete roles'
        }, 500


class RoleUpdateResource(Resource):
    def post(self):
        args = request.get_json()
        keys = args.get("keys")
        roles = get_roles(keys=keys)
        if not roles:
            return {
                "message": "Not role"
            }
        name = args.get("name")
        level = args.get('level', None)
        type = args.get('type', None)
        owner_keys = args.get('owner_keys', None)
        if type:
            type = RoleType(type)
        for role in roles:
            if not update_role(role, name=name, level=level, role_type=type):
                return {
                    'message': 'error'
                }

        if owner_keys is not None and not role_facade.update_roles_owners(roles, owner_keys=owner_keys):
            return {
                'message': "update owners error"
            }
        return {
            'message': 'ok'
        }


class RoleOwnerResource(Resource):
    def get(self):
        try:
            keys = request.args.getlist('keys', type=str)
            roles = role_facade.get_roles(keys=keys)
            if not roles:
                return {
                    'message': f"not roles"
                }, 400

            out = role_facade.get_roles_owners(roles=roles)
        except Exception as e:
            return {
                       'message': f"something error: {e}"
                   }, 500
        return out, 200

    def post(self):
        try:
            args = request.get_json()
            keys = args.get("keys")
            owner_keys = args.get("owner_keys")
            roles = role_facade.get_roles(keys=keys)
            if role_facade.update_roles_owners(roles, owner_keys):
                return {
                           'message': "ok"
                       }, 200
            return {
                       'message': "update role owner fail"
                   }, 500
        except Exception as e:
            return {
                       'message': f"something error: {e}"
                   }, 500


class RoleMemberDirctResource(RBACResource):
    # 更新成员包括user和role（替换的方式）
    def post(self):
        args = request.get_json()
        keys = args.get("keys", [])
        user_keys = args.get("user_keys", [])
        role_keys = args.get("role_keys", [])
        if not keys:
            return {
                       'message': 'ok'
                   }, 200
        owner_key = request.authorization.username
        if len(role_facade.judge_users_owned_roles(user_keys=[owner_key], role_keys=keys)[owner_key]) != len(keys) or not keys:
            return {
                       'message': 'you are not some roles owner'
                   }, 403

        if user_keys and not role_facade.set_roles_members(
                role_keys=keys, item_keys=user_keys, item_type=role_facade.item_facade.ItemType.user):
            return {
                       'message': 'set roles members fail'
                   }, 500
        if role_keys and not role_facade.set_roles_members(
                role_keys=keys, item_keys=role_keys, item_type=role_facade.item_facade.ItemType.role):
            return {
                       'message': 'set roles members fail'
                   }, 500
        return {
                   'message': "ok"
               }, 200

    # 获取现有成员，包括user和role
    def get(self):
        keys = request.args.getlist("keys", type=str)
        disable = request.args.get('disable', type=int, default=0)
        disable = ItemRefDisable(disable)
        owner_key = request.authorization.username
        out = dict()
        if len(role_facade.judge_users_owned_roles(user_keys=[owner_key], role_keys=keys)[owner_key]) != len(keys) \
                or not keys:
            return {
                       'message': 'you are not some roles owner'
                   }, 403
        out['users'] = role_facade.get_roles_members_direct(
            role_keys=keys, disable=disable, item_type=role_facade.item_facade.ItemType.user)
        out['roles'] = role_facade.get_roles_members_direct(
            role_keys=keys, item_type=role_facade.item_facade.ItemType.role, disable=disable)
        return out, 200

    def delete(self):
        args = request.get_json()
        keys = args.get("keys", [])
        user_keys = args.get("user_keys", [])
        role_keys = args.get("role_keys", [])
        if not keys:
            return {
                       'message': 'ok'
                   }, 200
        owner_key = request.authorization.username
        if len(role_facade.judge_users_owned_roles(user_keys=[owner_key], role_keys=keys)[owner_key]) != len(
                keys) or not keys:
            return {
                       'message': 'you are not some roles owner'
                   }, 403
        if role_facade.delete_roles_members(role_keys=keys, item_keys=user_keys, item_type=item_facade.ItemType.user) \
                and \
                role_facade.delete_roles_members(role_keys=keys, item_keys=role_keys, item_type=item_facade.ItemType.role):
            return {
                'msg': 'ok'
            }, 200
        return {
            'msg': 'something wrong'
        }, 500


class RoleMemberFlattenResource(RBACResource):
    def get(self):
        keys = request.args.getlist('keys', type=str)
        out = dict()
        for key in keys:
            out[key] = role_facade.get_role_members_flatten(key)
        return out, 200
