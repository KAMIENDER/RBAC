import logging

from flask import request, jsonify
from flask_restful import Resource
from pydantic.main import BaseModel

from domains.role.entity.value import RoleType
from domains.role.service.role_facade import create_role, get_roles, update_role


class RoleResource(Resource):
    class RoleModel(BaseModel):
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
            create_role(args)
        except Exception as e:
            logging.error(f"role resource create role error: {e}, args: {args}")
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
        if type:
            type = RoleType(type)
        for role in roles:
            if not update_role(role, name=name, level=level, type=type):
                return {
                    'message': 'error'
                }
        return {
            'message': 'ok'
        }
