from flask import Flask
from flask_restful import Api

from application.service.permission import PermissionBasicResource
from application.service.user import UserResource, UserUpdateResource


def register(app):
    register_user(app, pre_url='/user/')
    register_permission(app, pre_url='/permission/')


def register_user(app: Flask, pre_url: str = "/"):
    api = Api(app)
    api.add_resource(UserResource, pre_url+'resource/')
    api.add_resource(UserUpdateResource, pre_url+'update_user/')


def register_permission(app: Flask, pre_url: str = '/'):
    api = Api(app)
    api.add_resource(PermissionBasicResource, pre_url + 'resource/')
