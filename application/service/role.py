import logging
from typing import List

from flask import request, jsonify
from flask_restful import Resource
from pydantic.main import BaseModel

from domains.role.entity.value import RoleType
from domains.role.service.role_facade import create_role, get_roles, update_role
import domains.role.service.role_facade as role_facade

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
            out.append(dict(self.RoleModel.from_orm(role)))
        return {
            'data': out
        }


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
