from unittest import TestCase
import uuid
import sys #fixes import errors
import os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from instance.config import config
from app.models import User, Orders, Menu, db, Meals

class GroundTests(TestCase):
    '''The Founding tests for the DB'''
    def setUp(self):
        '''The first step for it's run'''
        self.app = create_app(config['testing'])
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.session.commit()
        db.drop_all()
        db.create_all()
 
        #Create a new user
        self.new_user = User(user_id = int(uuid.uuid4()), username="quantum", password="secret", admin=True)
        db.session.add(self.new_user)
        db.session.commit()

        #Add new meal
        self.new_meal = Meals(meal_id = int(uuid.uuid4()), meal_name = "Rice", meal_price = 200,
            meal_category = "lunch", meal_day = 'monday')
        db.session.add(self.new_meal)
        db.session.commit()

        #Add new meal 2
        self.new_meal = Meals(meal_id = int(uuid.uuid4()), meal_name = "beef", meal_price = 300,
            meal_category = "lunch", meal_day = 'tuesday')
        db.session.add(self.new_meal)
        db.session.commit()

        #Add meal to menu
        self.meal = Meals.query.filter_by(meal_name='Chips').first()
        self.new_menu = Menu(menu_id = self.meal.menu_id, menu_name = "Chips", menu_price = 200,
            menu_category = "lunch", menu_day = 'monday')
        db.session.add(self.new_menu)
        db.session.commit()

        #Add meal in menu to order
        self.menu = Menu.query.filter_by(menu_name='Rice').first()
        self.new_order = Orders(order_id = self.menu.menu_id, order_name = 'Rice ', order_price = 200,
            order_category = 'lunch', order_day = 'monday', order_qty=1, order_user = 'quantum')
        db.session.add(self.new_order)
        db.session.commit()

        #Add new meal 2
        self.new_meal2 = Meals(meal_id = int(uuid.uuid4()), meal_name = "Black Coffee", meal_price = 70,
            meal_category = "breakfast", meal_day = 'tuesday')
        db.session.add(self.new_meal2)
        db.session.commit()

        #Add meal to menu 2
        self.meal2 = Meals.query.filter_by(meal_name='Tea').first()
        self.new_menu2 = Menu(menu_id = self.meal2.meal_id, menu_name = "Milk with Bread", menu_price = 70,
            menu_category = "breakfast", menu_day = 'tuesday')
        db.session.add(self.new_menu2)
        db.session.commit()

        self.tester = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()