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
        self.meal = Meals.query.filter_by(meal_name='beef').first()
        self.new_menu = Menu(meal_relelation= self.meal, menu_id= uuid.uuid4())
        db.session.add(self.new_menu)
        db.session.commit()

        #Add meal in Items to order
        self.new_order = Orders(order_qty=4,meal_id= self.meal.meal_id)
        db.session.add(self.new_order)
        db.session.commit()

        #Add new meal 2
        self.new_meal2 = Meals(meal_id = uuid.uuid4(), meal_price='200', meal_name = "Black Coffee",
            meal_category = "breakfast", meal_day = 'tuesday')
        db.session.add(self.new_meal2)
        db.session.commit()

        #Add meal to menu 2
        self.meal2 = Meals.query.filter_by(meal_name='Tea').first()
        self.new_menu2 = Menu(meal_relelation= self.meal, menu_id= uuid.uuid4())
        db.session.add(self.new_menu2)
        db.session.commit()

        self.tester = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()