from app import app
import unittest
import json


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.data = {"name":"quantum", "email":"quantum@gmail.com","password":"secret","role":'user'}
        self.data1 = {"id":1,"name":"Chips","price":"1000",'role':'user'}
        self.data2 = {"id":1,"name":"Sea food","content":"Lobster,Prawn","price":"1500"}
        self.data3 = {"id":1,"name":"Order1","price":"15,000"}
        self.data4 = {"id":1,"name":"Today's Menu",'content':'lobster',"price":"1500"}


    def test_signup(self):
        response = self.app.post('/api/v1/auth/signup', data = json.dumps(self.data) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(result["name"], "quantum")
        self.assertEqual(result["email"], "quantum@gmail.com")
        self.assertEqual(result["password"], "secret")
        self.assertEqual(result["role"],"user")
        self.assertEqual(response.status_code, 201)
    
    def test_login(self):
        response = self.app.post('/api/v1/auth/signup', data = json.dumps(self.data) , content_type = 'application/json')
        response = self.app.post('/api/v1/auth/login', data = json.dumps(self.data) , content_type = 'application/json')
        result = json.loads(response.data )
        self.assertEqual(result["name"], "quantum")
        self.assertEqual(result["password"], "secret")
        self.assertEqual(result["role"],"user")
        self.assertEqual(response.status_code, 200)

    def test_admMealsOptions(self):
        response = self.app.get('/api/v1/meals/')
        result = json.loads(response.data)
        print(result)
        self.assertEqual(response.status_code, 200)
        
    def test_admPostMealsOptions(self):
        response = self.app.post('/api/v1/meals/<int:id>', data = json.dumps(self.data1) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "Chips")
        self.assertEqual(result["price"], "1000")
        self.assertEqual(result["role"],"user")
        self.assertEqual(response.status_code, 201)
    
    def test_admPutMealsOptions(self):
        response = self.app.put('/api/v1/meals/', data=json.dumps(self.data1), content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "Chips")
        self.assertEqual(result["price"], "1000")
        self.assertEqual(result["role"],"user")
        self.assertEqual(response.status_code, 201)

    def test_admDeleteMealOptions(self):
        response = self.app.delete('/api/v1/meals/', data=json.dumps(self.data1), content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
    
    #Test Menu
    def test_admGet_Menu(self):
        response = self.app.get('/api/v1/menu/')
        result = json.loads(response.data)
        print(result)
        self.assertEqual(response.status_code, 200)
        
    def test_admPost_Menu(self):
        response = self.app.post('/api/v1/menu/', data = json.dumps(self.data2) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "Sea food")
        self.assertEqual(result["content"], "Lobster,Prawn")
        self.assertEqual(result["price"], "1500")
        self.assertEqual(response.status_code, 200)
    
    def test_admPutMealsOptions(self):
        response = self.app.put('/api/v1/menu/', data=json.dumps(self.data2), content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "Sea food")
        self.assertEqual(result["content"], "Lobster,Prawn")
        self.assertEqual(result["price"], "1500")
        self.assertEqual(response.status_code, 201)

    def test_admDeleteMealOptions(self):
        response = self.app.delete('/api/v1/menu/', data=json.dumps(self.data2), content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
    #Check Orders

    def test_get_AdminCheckOrders(self):
        response = self.app.get('/api/v1/orders/')
        result = json.loads(response.data)
        print(result)
        self.assertEqual(response.status_code, 200)

    def test_Post_AdminCheckOrders(self):
        response = self.app.post('/api/v1/orders/', data = json.dumps(self.data3) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "Order1")
        self.assertEqual(result["content"], "15,000")
        self.assertEqual(response.status_code, 201)
    
    def test_Put_AdminCheckOrders(self):
        response = self.app.put('/api/v1/orders/', data=json.dumps(self.data3), content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "Order1")
        self.assertEqual(result["price"], "15,000")
        self.assertEqual(response.status_code, 201)
#Customer
    def test_get_custCheckMenu(self):
        response = self.app.get('/api/v1/user/menu/')
        result = json.loads(response.data)
        print(result)
        self.assertEqual(response.status_code, 200)

    def test_Post_AdminCheckOrders(self):
        response = self.app.post('/api/v1/user/menu/<int:id>', data = json.dumps(self.data4) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "Today's Menu")
        self.assertEqual(result["content"], "lobster")
        self.assertEqual(result['price'],"1500")
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()
