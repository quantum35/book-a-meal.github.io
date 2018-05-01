import unittest
import json
from app import app

 #Test Endpoints for the Endpoints
class TestFlaskAppEndpoints(unittest.TestCase):
    
    def setUp(self):
        
        self.tester = app.test_client()
        #register user first
        reg_data = json.dumps(
            {"user_id": 1, "username": "Quantum", "password": "pass123", "admin": False})
        response = self.tester.post(
            '/api/v1/auth/signup', data=reg_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        #Login the user
        log_data = json.dumps({"username": "Quantum", "password": "pass123"})
        response1 = self.tester.post(
            '/api/v1/auth/login', data=log_data, content_type='application/json')
        self.assertEqual(response1.status_code, 200)

        self.token = json.loads(response1.data)['message']

        self.headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    def test_get_users(self):
        #Test user access to the menu
        response = self.tester.get('/api/v1/users', headers=self.headers)
        self.assertEqual(response.status_code, 200)

    #User activities

    def test_user_signup(self):
        reg_data = json.dumps(
            {"user_id": 1, "username": "Quantum", "password": "pass123", "admin": False})
        response = self.tester.post(
            '/api/v1/auth/signup', data=reg_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_user_login(self):
        #Test the user login 
        #register user first
        reg_data = json.dumps(
            {"user_id": 1, "username": "Quantum", "password": "pass123", "admin": False})
        response = self.tester.post(
            '/api/v1/auth/signup', data=reg_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        #Login the user
        log_data = json.dumps({"username": "Quantum", "password": "pass123"})
        response1 = self.tester.post(
            '/api/v1/auth/login', data=log_data, content_type='application/json')
        self.assertEqual(response1.status_code, 200)

    def test_user_get_menu(self):
        response = self.tester.get('/api/v1/menu/', headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_user_post_order(self):
        meal_data = json.dumps(
            {"meal_id": 1, "meal_name": "Chips", "price": 2000, "category": "dinner", "day": "none"})
        response = self.tester.post(
            '/api/v1/meals/', data=meal_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)

        setup = self.tester.post(
            '/api/v1/menu/', data=meal_data, headers=self.headers)
        self.assertEqual(setup.status_code, 200)

        get_menu = self.tester.get('/api/v1/menu/', headers=self.headers)
        self.assertEqual(get_menu.status_code, 200)

        order_data = json.dumps({"meal_id": 1, "meal_name": "Rice", "price": 200,
                                 "category": "dinner", "day": "none", "quantity": 1, "username": "ian"})

        make_order = self.tester.post(
            '/api/v1/orders', data=order_data, headers=self.headers)
        self.assertEqual(make_order.status_code, 200)

    def test_user_put_order(self):
        meal_data = json.dumps(
            {"meal_id": 1, "meal_name": "Rice", "price": 200, "category": "dinner", "day": "none"})
        response = self.tester.post(
            '/api/v1/meals/', data=meal_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)

        setup = self.tester.post(
            '/api/v1/menu/', data=meal_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)

        order_data = json.dumps({"meal_id": 1, "meal_name": "Rice", "price": 200,
                                 "category": "dinner", "day": "none", "quantity": 1, "username": "ian"})

        make_order = self.tester.post(
            '/api/v1/orders', data=order_data, headers=self.headers)
        self.assertEqual(make_order.status_code, 200)

        mod_order = json.dumps({"quantity": 3})
        res = self.tester.put('/api/v1/orders/1',
                              data=mod_order, headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def test_caterer_get_mealoptions(self):
        response1 = self.tester.get('/api/v1/meals/', headers=self.headers)
        self.assertEqual(response1.status_code, 200)

    def test_caterer_post_mealoption(self):
        meal_data = json.dumps(
            {"meal_id": 1, "meal_name": "Rice", "price": 200, "category": "dinner", "day": "none"})
        response = self.tester.post(
            '/api/v1/meals/', data=meal_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_caterer_put_meal_option_by_id(self):
        meal_data = json.dumps(
            {"meal_id": 1, "meal_name": "Rice", "price": 200, "category": "dinner", "day": "none"})
        response = self.tester.post(
            '/api/v1/meals/', data=meal_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)

        update_data = json.dumps(
            {"meal_name": "Meat", "price": 210, "category": "lunch", "day": "Monday"})
        res = self.tester.put(
            '/api/v1/meals/1', data=update_data, headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def test_caterer_delete_mealoption_by_id(self):
        meal_data = json.dumps(
            {"meal_id": 8, "meal_name": "Rice", "price": 200, "category": "dinner", "day": "none"})
        response = self.tester.post(
            '/api/v1/meals/', data=meal_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)

        res = self.tester.delete('/api/v1/meals/8', headers=self.headers)
        self.assertEqual(res.status_code, 200)
   
    def test_caterer_setup_menu(self):
        meal_data = json.dumps(
            {"meal_id": 1, "meal_name": "Rice", "price": 200, "category": "dinner", "day": "none"})
        response = self.tester.post(
            '/api/v1/meals/', data=meal_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)

        setup = self.tester.post(
            '/api/v1/menu/', data=meal_data, headers=self.headers)
        self.assertEqual(setup.status_code, 200)

    def test_caterer_get_orders(self):
        res = self.tester.get('/api/v1/orders', headers=self.headers)
        self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
