from flask import  request, make_response
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from flask_restful import Resource
import jwt
from os import getenv
import datetime

from app.auth.tokens import token_required, admin_only
from app.models import User, Orders, Menu, db, Meals, Orders, Menu, db

class Signup(Resource):
    def post(self):
        post_data = request.get_json(force=True)

        if post_data['password'] == '' or post_data['username'] == '':
            return {'message': 'Please enter all the details'}

        if not isinstance(post_data['password'], str) or not isinstance(post_data['username'], str):
            return {'message': 'Please enter a string value for username and password'}

        hashed_password = generate_password_hash(
            post_data['password'], method='md5')
        new_user = User(user_id=str(uuid.uuid4()), username=post_data['username'],
                        password=hashed_password, admin=False)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'New user created!'}


    @admin_only
    def get(self, active_user):
    	users = User.query.all()
    	output = []
    	for user in users:
    		user_data = {}
    		user_data['user_id'] = user.user_id
    		user_data['username'] = user.username
    		user_data['password'] = user.password
    		output.append(user_data)

    	return {"status": "success", "data": output}, 200


class Login(Resource):
    """docstring for Login in Registered User"""

    def post(self):
        post_data = request.get_json(force=True)

        if post_data['password'] == '' or post_data['username'] == '':
            return {'message': 'Please enter all the details'}

        if not isinstance(post_data['password'], str) or not isinstance(post_data['username'], str):
            return {'message': 'Please enter a string value for username and password'}

        user = User.query.filter_by(username=post_data['username']).first()

        if not user:
            return {'message': 'Please sign up then login'}

        if check_password_hash(user.password, post_data['password']):
            token = jwt.encode({"user_id": user.user_id, "exp": datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=30)}, getenv('SECRET_KEY'))
            return {"token": token.decode('UTF-8')}

        return {"message": "wrong password, please try again"}
 
 
class MenuOrders(Resource):
    """docstring for MenuOrders"""
    @token_required
    def get(self, active_user):
        menu = Menu.query.all()
        output = []
        for meal in menu:
            data = {"menu":"id"}
            output.append(data)

        return {"status": "success", "data": output}, 200

    @token_required
    def post(self, active_user):
        post_data = request.get_json(force=True)
        meal = Menu.query.filter_by(menu_name=post_data['order_name']).first()

        if not meal:
            return {"message": "The meal was not found in menu"}

        order = Orders.query.filter_by(order_name=meal.menu_name).first()

        if order:
            return {"message": "The order exist!"}

        new_order = Orders(order_id=meal.menu_id, order_name=post_data['order_name'], order_price=post_data['order_price'],
                           order_category=post_data['order_category'], order_day=post_data['order_day'], order_qty=1, order_user=post_data['order_user'])
        #Add name from jwt
        db.session.add(new_order)
        db.session.commit()
        return {'message': 'Your order has been placed!'}

    @token_required
    def put(self, active_user, order_id):
        post_data = request.get_json(force=True)
        order = Orders.query.filter_by(order_id=order_id).first()

        if not order:
            return {"message": "The order was not found"}

        order.order_qty = post_data['order_qty']
        db.session.commit()

        return {"status": "success", "data": 'Order modified!'}, 200

    @token_required
    def delete(self, active_user, order_id):
        order = Orders.query.filter_by(order_id=order_id).first()

        if not order:
            return {"message": "The order was not found"}
        db.session.delete(order)
        db.session.commit()
        return {"message": "The order has been removed"}
class MealOptions(Resource):
    """docstring for Meal_man"""
    @admin_only
    def post(self, active_user):
        post_data = request.get_json(force=True)
        if post_data['meal_name'] == '' or post_data['meal_price'] == '':
            return {'message' : 'Please enter all the details'}

        if not isinstance(post_data['meal_name'], str):
            return {'message' : 'Please enter a string value for meal'}

        if not isinstance(post_data['meal_price'], int):
            return {'message' : 'Price should be a number'}

        new_meal = Meals(meal_id = str(uuid.uuid4()), meal_name = post_data['meal_name'], meal_price = post_data['meal_price'],
            meal_category = post_data['meal_category'], meal_day = post_data['meal_day'])
        db.session.add(new_meal)
        db.session.commit()
        return {'message' : 'New meal added!'}

    @admin_only
    def get(self, active_user):
        meals = Meals.query.all()
        output = []
        for meal in meals:
            meal_data = {}
            meal_data['meal_id'] = meal.meal_id
            meal_data['meal_name'] = meal.meal_name
            meal_data['meal_price'] = meal.meal_price
            meal_data['meal_category'] = meal.meal_category
            meal_data['meal_day'] = meal.meal_day
            output.append(meal_data)

        return {"status": "success", "data": output}, 200

    @admin_only
    def put(self, active_user, meal_id):
        post_data = request.get_json(force=True)
        meal = Meals.query.filter_by(meal_id=meal_id).first()

        if not meal:
            return {"message" : "The meal was not found"}

        if request.json['meal_name'] == '' or request.json['meal_price'] == '':
            return {'message' : 'Please enter all the details'}

        if not isinstance(request.json['meal_name'], str):
            return {'message' : 'Please enter a string value for meal'}

        meal.meal_name = post_data['meal_name']
        meal.meal_price = post_data['meal_price']
        meal.meal_category = post_data['meal_category']
        meal.meal_day = post_data['meal_day']
        db.session.commit()

        return {"status": "success", "data": 'Meal modified!'}, 200

    @admin_only
    def delete(self, active_user, meal_id):
        meal = Meals.query.filter_by(meal_id=meal_id).first()

        if not meal:
            return {"message" : "The meal was not found"}
        db.session.delete(meal)
        db.session.commit()
        return {"message" : "The meal has been deleted"}

class MenuOptions(Resource):
	"""docstring for Menu"""
	@admin_only
	def post(self, active_user):
		post_data = request.get_json(force=True)
		meal = Meals.query.filter_by(meal_name=post_data['menu_name']).first()

		if not meal:
			return {"message" : "The meal was not found"}

		new_menu = Menu(menu_id = meal.meal_id, menu_name = post_data['menu_name'], menu_price = post_data['menu_price'], menu_category = post_data['menu_category'], menu_day = post_data['menu_day'])
		db.session.add(new_menu)
		db.session.commit()
		return {'message' : 'New meal added to the menu!'}

class OrdersAll(Resource):
	"""docstring for Orders"""
	@admin_only
	def get(self, active_user):
		orders = Orders.query.all()
		output = []
		for order in orders:
			order_data = {}
			order_data['order_id'] = order.order_id
			order_data['order_name'] = order.order_name
			order_data['order_price'] = order.order_price
			order_data['order_category'] = order.order_category
			order_data['order_day'] = order.order_day
			order_data['order_qty'] = order.order_qty
			order_data['order_user'] = order.order_user
			output.append(order_data)
		return {"status": "success", "data": output}, 200
