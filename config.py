import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345@localhost:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
