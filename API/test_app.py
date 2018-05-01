import unittest
from app import *
from project.models.user import User
from project.models.caterer import Caterer
 
#Flask Test
class TestFlaskApp(unittest.TestCase):

	def test_create_users(self):
		#Test if any of the entered values are empty
		results = User().signup('', '1234567',7624)
		self.assertEqual(results, 'Please fill all the details',
		                 msg='There is an empty input')

		#Type check the data
		results4 = User().signup(45, 1234567,7624)
		self.assertEqual(
			results4, 'Please enter a string value for username and password')

		results5 = User().signup('quantum', '1234567', '9805')
		self.assertEqual(results5, 'User Id should be an integer!')

		#Creating a new user
		results1 = User().signup('quantum', '1234567',7624)
		self.assertEqual(results1, 'User successfully created',
		                 msg='Successful registration')

	def test_login_works_well(self):
		#Checking if all inputs are filled
		results = User().login('quantum', '')
		self.assertEqual(results, 'Enter both username and password',
		                 msg='You need to enter both username and password')

		#Type check the data
		results1 = User().login(45, 1234567)
		self.assertEqual(
			results1, 'Please enter a string value for username and password')

	def test_user_login(self):
		#Creating a new user
		User().signup('test', '1234567',7624)
		#Correct login from new user
		results = User().login('test', '1234567')
		self.assertIsInstance(results, str, msg='Incorrect output type')
#

	def test_post_meal(self):
		#Test if any of the entered values are empty
		results = Caterer().post_meal(1, "", 200, "", "Friday")
		self.assertEqual(results, 'Please enter all the details',
		                 msg='There is an empty input')

		#Creating a new meal
		results1 = Caterer().post_meal(1, "Kukutu", 200, "dinner", "Friday")
		self.assertEqual(results1, 'Meal successfully created',
		                 msg='Successful addition of meal')

		#Checking if the meal already exists
		results2 = Caterer().post_meal(1, "Kukutu", 200, "dinner", "Friday")
		self.assertEqual(results2, 'Meal exists!', msg='The meal already exists')

	def test_get_meal(self):
		Caterer().post_meal(1, "Kuku", 200, "lunch", "Friday")
		results = Caterer().get_meals()
		self.assertIsInstance(results, list, msg='Incorrect output type')

	def test_edit_meal(self):
		#Creating a new meal
		Caterer().post_meal(1, "Chicken", 200, "dinner", "Monday")

		#Modify meal
		results = Caterer().modify_meal(1, "beef", 200, "dinner", "Tuesday")
		self.assertEqual(results, 'Meal modification successful',
		                 msg='The meal was modified successfully')

	def test_delete_meal(self):
		#Creating a new meal
		Caterer().post_meal(3, "Chicken", 200, "dinner", "Monday")

		#Check if meal doesn't exists
		results = Caterer().delete_ml(2)
		self.assertEqual(results, 'Meal unavailable!',
		                 msg='The meal does not exist exists')

		#Modify meal
		results = Caterer().delete_ml(3)
		self.assertEqual(results, 'Meal Deleted successfully',
		                 msg='The meal was deleted successfully')

	def test_post_menu(self):
		#Check empty values are accepted
		results = Caterer().post_menu(4, '', 250, '', "Monday")
		self.assertEqual(results, 'Please enter all the details',
		                 msg='There is an empty input')

		#Post a menu
		results1 = Caterer().post_menu(5, "Ugali", 300, "lunch", "Monday")
		self.assertEqual(results1, 'Meal successfully added to menu')

		#Check if it's in the menu
		results2 = Caterer().post_menu(5, "Ugali", 300, "lunch", "Monday")
		self.assertEqual(results2, 'Meal exists in menu!')

	def test_get_orders(self):
		Caterer().post_menu(4, "Ugali", 250, "lunch", "Monday")
		User().make_order(4, "Ugali", 250, "lunch", "Monday", 1, "quantum")
		results = Caterer().get_orders()
		self.assertIsInstance(results, list, msg='Incorrect output type')

	def test_get_menu(self):
		#Post menu
		Caterer().post_menu(6, "Ugali", 300, "lunch", "Monday")

		results = User().get_menu()
		self.assertIsInstance(results, list, msg='Incorrect output type')

	def test_make_order(self):
		Caterer().post_menu(4, "Ugali", 250, "lunch", "Monday")
		results = User().make_order(4, "Ugali", 250, "lunch", "Monday", 1, "quantum")
		self.assertEqual(results, 'Meal successfully added ')

	def test_modify_order(self):
		Caterer().post_menu(7, "Ugali", 250, "lunch", "Monday")
		User().make_order(7, "Ugali", 250, "lunch", "Monday", 1, "quantum")

		#Check if meal exists
		results = User().modify_order(3, 3)
		self.assertEqual(results, 'Meal doesn\'t exists in orders!')

		#Modify meal
		results = User().modify_order(7, 3)
		self.assertEqual(results, 'Order  modified Succesfully')

	# def test_remove_order(self):
    # 	Caterer().post_menu(8, "Ugali", 250, "lunch", "Monday")
	# 	User().make_order(8, "Ugali", 250, "lunch", "Monday", 1, "quantum")

	# 	#Check if meal exists
	# 	results = User().remove_order(3)
	# 	self.assertEqual(results, 'Meal doesn\'t exists in orders!')

	# 	#Modify meal
	# 	results = User().remove_order(8)
	# 	self.assertEqual(results, 'Order removed successfully')


if __name__ == '__main__':
	unittest.main()
