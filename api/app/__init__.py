from flask import Flask
from flask_restful import Api
from app.views.routes import Signup, Login, MenuOrders, MealOptions, MenuOptions, OrdersAll
from instance.config import config


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    api = Api(app)

    from app.models import db
    db.init_app(app)

    api.add_resource(Signup, '/api/v1/auth/signup', '/api/v1/users')
    api.add_resource(Login, '/api/v1/auth/login')
    api.add_resource(MealOptions, '/api/v1/meals/', '/api/v1/meals/<string:meal_id>')
    api.add_resource(MenuOptions, '/api/v1/menu/')
    api.add_resource(OrdersAll, '/api/v1/orders')
    api.add_resource(MenuOrders, '/api/v1/menu/', '/api/v1/orders',
    	                '/api/v1/orders/<string:order_id>', '/api/v1/orders/<string:order_id>')

    return app


app = create_app(config['development'])
