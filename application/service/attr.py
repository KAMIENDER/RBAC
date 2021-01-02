from flask import request
from flask_restful import Resource

from domains.attr.entity.const import AttrDisable
import domains.attr.service.attr_facade as attr_facade


class AttrBasicResource(Resource):
    def get(self):
        args = request.args
        try:
            attr_key = args.get("attr_key", type=str)
            disable = args.get('disable', 1, type=int)
            if disable:
                disable = AttrDisable(disable)
        except:
            return {
                       'message': 'args error'
                   }, 400
        out = [item.key for item in attr_facade.get_attributes_by_like_key(attr_key, disable)]
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
