from flask import Flask
from flask_restful import Api

from application.service.permission import PermissionBasicResource
from application.service.role import RoleResource, RoleUpdateResource
from application.service.user import UserResource, UserUpdateResource


def register(app):
    register_user(app, pre_url='/user/')
    register_permission(app, pre_url='/permission/')
    register_role(app, pre_url='/role/')


def register_user(app: Flask, pre_url: str = "/"):
    api = Api(app)
    api.add_resource(UserResource, pre_url+'resource/')
    api.add_resource(UserUpdateResource, pre_url+'update_user/')


def register_permission(app: Flask, pre_url: str = '/'):
    api = Api(app)
    api.add_resource(PermissionBasicResource, pre_url + 'resource/')


def register_role(app: Flask, pre_url: str = "/"):
    api = Api(app)
    api.add_resource(RoleResource, pre_url+'resource/')
    api.add_resource(RoleUpdateResource, pre_url+'update_role/')