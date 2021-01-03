from flask import request
from flask_restful import Resource

from domains.attr.entity.const import AttrDisable
import domains.attr.service.attr_facade as attr_facade
from domains.item.entity.const import ItemType


class AttrBasicResource(Resource):
    def get(self):
        args = request.args
        try:
            attr_key = args.get("attr_key", type=str)
            disable = args.get('disable', 0, type=int)
            if disable is not None:
                disable = AttrDisable(disable)
        except:
            return {
                       'message': 'args error'
                   }, 400
        out = [item.key for item in attr_facade.get_attrs_by_key(like_key=attr_key, disable=disable)]
        return {
                   'attr_keys': out
               }, 200

    def post(self):
        args = request.get_json()
        try:
            attr_key = args.get('attr_key') or None
            if not attr_key:
                return {
                           'message': 'need more args'
                       }, 403
        except:
            return {
                       'message': 'args error'
                   }, 400
        if not attr_facade.create_attr(attr_key):
            return {
                       'message': 'create attr fail'
                   }, 403
        return {
                   'message': 'ok'
               }, 200


class AttrRelationResource(Resource):
    def get(self):
        args = request.args
        try:
            is_user = args.get("search_user", type=int, default=0)
            is_role = args.get("search_role", type=int, default=0)
            is_permission = args.get("search_permission", type=int, default=0)
            expression = args.get('expression', type=str, default="")
            disable = args.get('disable', type=int, default=0)
            if not expression or not (is_role or is_user or is_permission):
                return {
                           'message': 'need more args'
                       }, 403
            if disable is not None:
                disable = AttrDisable(disable)
        except:
            return {
                       'message': 'args error'
                   }, 400
        user_keys = list()
        role_keys = list()
        permission_keys = list()
        if is_user:
            user_keys = [user.key for user in
                         attr_facade.get_items_by_attr(expression=expression, item_type=ItemType.user, disable=disable)]
        if is_role:
            role_keys = [role.key for role in
                         attr_facade.get_items_by_attr(expression=expression, item_type=ItemType.role, disable=disable)]
        if is_permission:
            permission_keys = [permission.key for permission in
                               attr_facade.get_items_by_attr(expression=expression, item_type=ItemType.permission,
                                                             disable=disable)]
        return {
                   'user_keys': user_keys,
                   'role_keys': role_keys,
                   'permission_keys': permission_keys
               }, 200

    def post(self):
        args = request.get_json()
        try:
            attr_keys = args.get('attr_keys') or None
            user_keys = args.get('user_keys') or None
            role_keys = args.get('role_keys') or None
            permission_keys = args.get('permission_keys') or None
            value = args.get('value') or None
            if not attr_keys or not (user_keys or role_keys or permission_keys) or not value:
                return {
                           'message': 'need more args'
                       }, 403
        except:
            return {
                       'message': 'args error'
                   }, 400
        result = True
        if user_keys:
            result = result & attr_facade.set_attrs_to_items(user_keys, ItemType.user, attr_keys, value)
        if role_keys:
            result = result & attr_facade.set_attrs_to_items(role_keys, ItemType.role, attr_keys, value)
        if permission_keys:
            result = result & attr_facade.set_attrs_to_items(permission_keys, ItemType.permission, attr_keys, value)
        if not result:
            return {
                       'message': 'create attr fail'
                   }, 403
        return {
                   'message': 'ok'
               }, 200
