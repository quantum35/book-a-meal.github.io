from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
from os import getenv

# initialize sql-alchemy
db = SQLAlchemy()


class User(db.Model):
	"""docstring for General Users"""
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key = True, nullable=False)
	public_user_id = db.Column(db.String, nullable=False)
	name = db.Column(db.String(50), nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False )
	password = db.Column(db.String(80), nullable=False)
	# conf_password = db.Column(db.String(80), nullable=False)
	address = db.Column(db.String(120), nullable=False)
	admin = db.Column(db.Boolean, default = True)
	#user
	order_placed = db.relationship('Orders', backref='users', lazy=True)

	#admin
	menu_added = db.relationship('Menu', backref='users', lazy=True)
	#admin
	
	def __init__(self, public_user_id, name, email, password, address):
		self.name = name
		self.email = email
		self.password = password
		self.public_user_id = public_user_id
		self.address = address

	def __repr__(self):	
		'''db string for representing the user Object'''

		return '<User {}>'.format(self.user_id)

	@staticmethod
	def promote_user(user):
			user.admin = True
			user.save()


class Meals(db.Model):
	"""docstring for Meals"""
	__tablename__ = "meals"
	id = db.Column(db.Integer, primary_key = True)
	meal_id = db.Column(db.String(50), unique = True)
	meal_name = db.Column(db.String(50))
	meal_price = db.Column(db.Integer)
	meal_category = db.Column(db.String(50))
	menu_id = db.relationship('Menu', backref='meals', lazy=True)

	def __init__(self, meal_id,
				 meal_name,
				 meal_price, meal_category):
		self.meal_id = meal_id
		self.meal_name = meal_name
		self.meal_price = meal_price
		self.meal_category = meal_category

	def __repr__(self):
		return '<Meals {}>'.format(self.meal_id)

class Menu(db.Model):
	"""docstring for Meals"""
	__tablename__ = "menu"
	id = db.Column(db.Integer, primary_key = True)
	menu_id = db.Column(db.String(50), unique = True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
	
	
	def __init__(self, menu_id):
		self.menu_id = menu_id

	def __repr__(self):
		return '<Menu {}>'.format(self.menu_id)

class Orders(db.Model):
	"""docstring for Orders"""
	__tablename__ = "orders"
	id = db.Column(db.Integer, primary_key = True)
	order_id = db.Column(db.String(50), unique = True)
	order_date = db.Column(db.DateTime, default=datetime.today())
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)

	def __init__(self, order_id):
		self.order_id = order_id

	def __repr__(self):
		return '<Orders {}>'.format(self.order_id)
