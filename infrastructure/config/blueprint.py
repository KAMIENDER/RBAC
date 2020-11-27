from flask import Flask


def register_user(app: Flask, pre_url: str = "user/"):
    api = Api