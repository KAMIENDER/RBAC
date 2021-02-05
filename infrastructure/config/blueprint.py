from flask import Flask
from flask_restful import Api

from application.service.attr import AttrBasicResource, AttrRelationResource
from application.service.permission import PermissionBasicResource, PermissionAuthResource, PermissionUpdateResource, \
    PermissionOwnerResource
from application.service.role import RoleResource, RoleUpdateResource, RoleOwnerResource, RoleMemberDirctResource, \
    RoleMemberFlattenResource, RoleMemberBeLongResource, RoleMemberBeLongFlattenResource
from application.service.user import UserResource, UserUpdateResource


def register(app):
    register_user(app, pre_url='/user/')
    register_permission(app, pre_url='/permission/')
    register_role(app, pre_url='/role/')
    register_attr(app, pre_url='/attr/')


def register_user(app: Flask, pre_url: str = "/"):
    api = Api(app)
    api.add_resource(UserResource, pre_url+'resource/')
    api.add_resource(UserUpdateResource, pre_url+'update_user/')


def register_permission(app: Flask, pre_url: str = '/'):
    api = Api(app)
    api.add_resource(PermissionBasicResource, pre_url + 'resource/')
    api.add_resource(PermissionAuthResource, pre_url + 'auth/')
    api.add_resource(PermissionUpdateResource, pre_url + 'update/')
    api.add_resource(PermissionOwnerResource, pre_url + "owner/")


def register_role(app: Flask, pre_url: str = "/"):
    api = Api(app)
    api.add_resource(RoleResource, pre_url+'resource/')
    api.add_resource(RoleUpdateResource, pre_url+'update_role/')
    api.add_resource(RoleOwnerResource, pre_url+'owner/')
    api.add_resource(RoleMemberDirctResource, pre_url+'member/')
    api.add_resource(RoleMemberFlattenResource, pre_url + 'flatten_member/')
    api.add_resource(RoleMemberBeLongResource, pre_url + 'belong_role/direct/')
    api.add_resource(RoleMemberBeLongFlattenResource, pre_url + 'belong_role/flatten/')


def register_attr(app: Flask, pre_url: str = "/"):
    api = Api(app)
    api.add_resource(AttrBasicResource, pre_url+'resource/')
    api.add_resource(AttrRelationResource, pre_url+'relation/')