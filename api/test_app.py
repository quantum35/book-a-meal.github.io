from app import app
import unittest
import json


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.data = {"username":"quantum", "email":"quantum@gmail.com","password":"password"}
        self.data1 = {"meal_id":"meal1", "name":"Chips","price":"1000"}
        self.data11 = {"meal_id":"meal1", "name":"Ugali","price":"500"}
        self.data2 = {"meal_id":"meal1", "name":"Ugali","price":"500"}
        self.data3 = {"meal_id":"meal1", "name":"Chips","price":"1000"}
        self.data4 = {"name":"ugali", "price":"1000"}
        self.data12 = {'id':'1','name':'Rice','price':'400'}

    def test_login(self):
        response = self.app.post('/auth/login', data = json.dumps(self.data) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(result["email"], "quantum@gmail.com")
        self.assertEqual(result["password"], "password")
        self.assertEqual(response.status_code, 201)

    def test_signup(self):
        response = self.app.post('/auth/signup', data = json.dumps(self.data) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(result["username"], "quantum")
        self.assertEqual(result["email"], "quantum@gmail.com")
        self.assertEqual(result["password"], "password")
        self.assertEqual(response.status_code, 201)
    
    def test_addNewMeal(self):
        response = self.app.post('/meals/', data = json.dumps(self.data2) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(result["meal_id"], "meal1")
        self.assertEqual(result["name"], "Chips")
        self.assertEqual(result["price"], "1000")
        self.assertEqual(response.status_code, 201)

    def test_modifyMeal(self):
        response = self.app.put('/meals/1', data = json.dumps(self.data11) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(result["meal_id"], "meal1")
        self.assertEqual(result["name"], "Ugali")
        self.assertEqual(result["price"], "500")
        self.assertEqual(response.status_code, 201)

    def test_deleteMealOption(self):
        response = self.app.delete('/meals/1',data=json.dumps(self.data1),content_type = 'application/json' )
        result = json.loads(response.data)
        self.assertEqual(result["message"], "Meal Successfuly Deleted")
        self.assertEqual(response.status_code, 200)

    def test_MealOfTheDay(self):
        response = self.app.post('/menu/', data = json.dumps(self.data1) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(result["meal_id"], "meal1")
        self.assertEqual(result["name"], "Chips")
        self.assertEqual(result["price"], "1000")
        self.assertEqual(response.status_code, 201)
    
    def test_OrdersMadeByUsers(self):
        response = self.app.get('/orders/')
        result = json.loads(response.data)
        self.assertEqual(result["message"], "Here are The Orders Made by users")
        self.assertEqual(response.status_code, 200)

    def test_profitMade(self):
        response = self.app.get('/profit')
        result = json.loads(response.data)
        self.assertEqual(result["message"], "Todays Profit is")
        self.assertEqual(response.status_code, 200)

    def test_admCheckOrderHistory(self):
        response = self.app.get('/orders')
        result = json.loads(response.data)
        self.assertEqual(result["message"], "Here is Your History")
        self.assertEqual(response.status_code, 200)

    def test_noAdmin(self):
        response = self.app.get('/admin/')
        result = json.loads(response.data)
        self.assertEqual(result["message"], "Return More Than one Admin Loged In")
        self.assertEqual(response.status_code, 200)

#Cutomers Test
    def test_custCheckDaysMenu(self):
        response = self.app.get('/users/menu/')
        result = json.loads(response.data)
        self.assertEqual(result["message"], "Here is your Menu Of the Day")
        self.assertEqual(response.status_code, 200)

    def test_changeMealChoice(self):
        response = self.app.put('/menu/1', data = json.dumps(self.data4) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(result["name"], "Ugali")
        self.assertEqual(result["price"], "500")
        self.assertEqual(response.status_code, 201)

    def test_checkOrderHistory(self):
        response = self.app.get('/users/orders')
        result = json.loads(response.data)
        self.assertEqual(result["message"], "Here is your Order History")
        self.assertEqual(response.status_code, 200)

    def test_getNotification(self):
        response = self.app.get('/users/notification')
        result = json.loads(response.data)
        self.assertEqual(result["message"], "You have one New Message")
        self.assertEqual(response.status_code, 200)
        
    def test_modifyOrder(self):
        response = self.app.put('/users/orders/1', data = json.dumps(self.data12) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(result["id"], "1")
        self.assertEqual(result["name"], "Rice")
        self.assertEqual(result["price"], "400")
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()
