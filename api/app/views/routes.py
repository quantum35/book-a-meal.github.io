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

        if post_data['password'] == '' or post_data['name'] == '' or post_data['email'] == '' or post_data['confirm_password']=='':
            return {'message': 'Please enter all the details'}

        if not isinstance(post_data['password'], str) or not isinstance(post_data['name'], str):
            return {'message': 'Please enter a string value for Name and password'}

        hashed_password = generate_password_hash(
            post_data['password'], method='md5')
        conf_hashed_password = generate_password_hash(
            post_data['confirm_password'], method='md5'
        )
        print(hashed_password)
        print(conf_hashed_password)
        if check_password_hash(hashed_password, conf_hashed_password):
            return {'message':'Make sure The password are the same'}
        new_user = User(public_user_id=str(uuid.uuid4()), name=post_data['name'],
                        password=hashed_password, email=post_data['email'], address=post_data['address'])
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

        if post_data['password'] == '' or post_data['email'] == '':
            return {'message': 'Please enter all the details'}

        if not isinstance(post_data['password'], str) or not isinstance(post_data['email'], str):
            return {'message': 'Please enter a string value for Email and password'}

        user = User.query.filter_by(email=post_data['email']).first()

        if not user:
            return {'message': 'Please sign up then login'}

        if check_password_hash(user.password, post_data['password']):
            token = jwt.encode({"public_user_id": user.public_user_id, "exp": datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=30)}, getenv('SECRET_KEY'))
            return {"token": token.decode('UTF-8')}

        return {"message": "wrong password, please try again"}


class MealOptions(Resource):
    """docstring for For Admin Manipulating the meal Options I.e Deleting,Editing,Posting a meal"""
    @admin_only
    def post(self, active_user):
        post_data = request.get_json(force=True)
        # if post_data['meal_name'] == '' or post_data['meal_price'] == '' or post_data['meal_category']:
        #     return {'message': 'Please enter all the details'}
        try:
            if not isinstance(post_data['meal_name'], str):
                return {'message': 'Please enter a string value for meal'}
            
            check_meal = Meals.query.filter_by(meal_name = post_data['meal_name']).first()
            if check_meal:
                return {'message':"Meal With that name already Exist"}
            
            if post_data['meal_name']=='' or post_data['meal_category']=='':
                return {'message':'Fill the blanks'}

            if not isinstance(post_data['meal_price'], int):
                return {'message': 'Price should be a number'}

            new_meal = Meals(meal_id=str(uuid.uuid4()), meal_name=post_data['meal_name'], meal_price=post_data['meal_price'],
                            meal_category=post_data['meal_category'])
            db.session.add(new_meal)
            db.session.commit()
            return {'message': 'New meal Successfully added!'}

        except print(0):
            pass

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
            output.append(meal_data)

        return {"status": "success", "data": output}, 200

    @admin_only
    def put(self, active_user, meal_id):
        post_data = request.get_json(force=True)
        meal = Meals.query.filter_by(meal_id=meal_id).first()

        if not meal:
            return {"message": "The meal was not found"}

        if request.json['meal_name'] == '' or request.json['meal_price'] == '' or request.json['meal_category']:
            return {'message': 'Please enter all the details'}

        if not isinstance(request.json['meal_name'], str):
            return {'message': 'Please enter a string value for meal'}

        meal.meal_name = post_data['meal_name']
        meal.meal_price = post_data['meal_price']
        meal.meal_category = post_data['meal_category']
        db.session.commit()

        return {"status": "success", "data": 'Meal modified!'}, 200

    @admin_only
    def delete(self, active_user, meal_id):
        meal = Meals.query.filter_by(meal_id=meal_id).first()

        if not meal:
            return {"message": "The meal was not found"}
        db.session.delete(meal)
        db.session.commit()
        return {"message": "The meal has been Successfully deleted"}


class MenuOptions(Resource):
    """docstring for Admin Setting up Menu Of the Day and Users Getting menu of the Day"""
    @admin_only
    def post(self, active_user):
        post_data = request.get_json(force=True)
        meal = Menu.meal_id
        if post_data == meal.meal_name:
            db.session.add(meal)
            db.session.commit()
            return {'message': 'New meal added to the menu!'}
        else:
            return {"message" : "Meal With That Name was not found"}


class MenuOrders(Resource):
    """docstring for MenuOrders"""
    @token_required
    def get(self, active_user):
        menu = Menu.query.all()
        output = []
        for meal in menu:
            data = {}
            data['menu_name'] = meal.menu_name
            data['menu_price'] = meal.menu_price
            data['menu_category'] = meal.menu_category
            output.append(data)

        return {"status": "success", "data": output}, 200

    @token_required
    def post(self, active_user):
        data = request.get_json(force=True)
        order = Orders.menu_id
        
        if order:
            db.session.add(order)
            db.session.commit()
            
            return {'message': 'Order Successfully Placed!'}
        else:
            return {"message": "Order Not Placed"}


    # @token_required
    # def put(self, active_user, order_id):
    #     post_data = request.get_json(force=True)
    #     order = Orders.query.filter_by(order_id=order_id).first()

    #     if not order:
    #         return {"message": "The order was not found"}

    #     order.order_qty = post_data['order_qty']
    #     db.session.commit()

    #     return {"status": "success", "data": 'Order modified!'}, 200

    # @token_required
    # def delete(self, active_user, order_id):
    #     order = Orders.query.filter_by(order_id=order_id).first()

    #     if not order:
    #         return {"message": "The order was not found"}
    #     db.session.delete(order)
    #     db.session.commit()
    #     return {"message": "The order has been removed"}



class OrdersAll(Resource):
	"""docstring for Orders"""
	@admin_only
	def get(self, active_user):
		orders = Orders.query.all()
		output = []
		for order in orders:
			order_data = {}
			order_data['order_id'] = orders.order_id
			order_data['Placed By'] = orders.user_id
			order_data['meals'] = orders.menu_id.meal_id.meal_name
			order_data['order_category'] = order.order_category
			order_data['order_day'] = order.order_day
			order_data['order_qty'] = order.order_qty
			order_data['order_user'] = order.order_user
			output.append(order_data)
		return {"status": "success", "data": output}, 200
