from flask import Flask
from flask_restful import Api

from application.service.user import UserReource

def register(app):
    register_user(app, pre_url='/user/')

def register_user(app: Flask, pre_url: str = "/"):
    api = Api(app)
    api.add_resource(UserReource, pre_url+'register/')