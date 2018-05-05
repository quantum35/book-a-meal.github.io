from os import getenv
from flask import Flask
from flask_restful import Api
from datetime import timedelta
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity,exceptions
)

#local Imports
from app.views.authenticate import Signup, Login 
from app.views.meals import MealOptions, MealLists
from app.views.menu  import MenuOptions, MenuList
from app.views.orders import Orders, OrderLists
from instance.config import config

jwt = JWTManager()

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    api = Api(app)
    app.config['JWT_SECRET_KEY'] = getenv('SECRET_KEY');
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=72)
    jwt.init_app(app)

    from app.models import db
    db.init_app(app)

    api.add_resource(Signup, '/api/v2/auth/signup')
    api.add_resource(Login, '/api/v2/auth/login')
    api.add_resource(MealOptions,'/api/v2/meals/<int:id>')
    api.add_resource(MealLists, '/api/v2/meals')
    api.add_resource(MenuOptions,'/api/v2/menus/<int:id>')
    api.add_resource(MenuList, '/api/v2/menus')
    api.add_resource(Orders,  '/api/v2/orders/<int:id>')
    api.add_resource(OrderLists, '/api/v2/orders')
    



    return app


app = create_app(config['development'])
