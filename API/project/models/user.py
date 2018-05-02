from flask import session
from project.models.caterer import Caterer
import datetime
import jwt


class User(object):
	"""docstring for Users"""
	users = [
				{'username': 'user', 'password': 'user123', 'user_id': 178, 'admin': False},
				{'username': 'admin', 'password': 'admin123', 'user_id': 7625, 'admin': True}
			]

	def __init__(self):
		self.output = {}

	def signup(self, username, password, user_id):
    		#checks if the User password and nam field is blank
		if username == '' or password == '' or user_id == '':
			return 'Please fill all the details'

		if not isinstance(username, str) or not isinstance(password, str):
			return 'Please enter a string value for username and password'
		if not isinstance(user_id, int):
			return 'User Id should be an integer!'

		#If the Sigup is success
		user = [u for u in User().users if u["username"] ==
                    username and u['user_id'] == user_id]
		if user:
			return 'User exists with that username already exist!'

		self.output['username'] = username
		self.output['password'] = password
		self.output['user_id'] = user_id
		self.output['admin'] = False
		User.users.append(self.output)
		return 'User successfully created'

	def login(self, username, password):
		if username == '' or password == '':
			return 'Enter both username and password'

		if not isinstance(username, str) or not isinstance(password, str):
			return 'Please enter a string value for username and password'

		logged_user = [u for u in User().users if u["username"] ==
                    username and u["password"] == password]
		user = logged_user[0]

		if logged_user:
			token = jwt.encode({
				"user_id": user["user_id"],
				"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'Quantum#@$%^^&$#@@')
			return token.decode('UTF-8')

		return 'No such user! Sign Up'

	def logout(self):
		session['logged_in'] = False
		if session['logged_in'] == False:
			return 'Log out successful'

	def show_users(self):
		return User().users

	def get_menu(self):
		return Caterer().menu_list

	def make_order(self, meal_id, meal_name, price, category, day, quantity, username):
		if meal_id == '' or meal_name == '' or price == '' or category == '' or day == '' or quantity == '' or username == '':
			return 'Please enter all the details'

		#Should validate the input data types
		menus = [menu for menu in Caterer().menu_list if menu["meal_id"] ==
                    meal_id and menu['meal_name'] == meal_name]
		if not menus:
			return 'Meal doesn\'t exists in menu!'

		self.output['meal_id'] = meal_id
		self.output['meal_name'] = meal_name
		self.output['price'] = price
		self.output['category'] = category
		self.output['day'] = day
		self.output['quantity'] = quantity
		self.output['username'] = username
		Caterer.order_list.append(self.output)
		return 'Meal successfully added '

	def modify_order(self, meal_id, quantity):
	    #Should validate the input data types
	    orders = [order for order in Caterer(
	    ).order_list if order["meal_id"] == meal_id]
	    if not orders:
	    	return 'Meal doesn\'t exists in orders!'

	    orde = orders[0]
	    price = orde["price"]

	    self.output['quantity'] = quantity
	    self.output['price'] = price * quantity
	    return 'Order  modified Succesfully'

	def remove_order(self, meal_id):
		orders = [order for order in Caterer(
		).order_list if order["meal_id"] == meal_id]
		if not orders:
			return 'Meal doesn\'t exists in orders!'

		Caterer.order_list.remove(orders[0])
		return 'Order removed successfully'
