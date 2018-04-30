import os
basedir = os.path.abspath(os.path.dirname(__name__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "postgres://localhost:5432"
#This is end of Config file