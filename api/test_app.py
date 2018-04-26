from app import app
import unittest
import json


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.data = {"name":"quantum", "email":"quantum@gmail.com","password":"secret"}
        self.data1 = {"id":"1","name":"Chips","price":"1000"}
        self.data2 = {"id":"1","name":"Sea food","content":"Lobster,Prawn"}

    def test_signup(self):
        response = self.app.post('/api/v1/auth/signup', data = json.dumps(self.data) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(result["name"], "quantum")
        self.assertEqual(result["email"], "quantum@gmail.com")
        self.assertEqual(result["password"], "secret")
        self.assertEqual(response.status_code, 201)
    
    def test_login(self):
        response = self.app.post('/api/v1/auth/signup', data = json.dumps(self.data) , content_type = 'application/json')
        response = self.app.post('/api/v1/auth/login', data = json.dumps(self.data) , content_type = 'application/json')
        result = json.loads(response.data )
        self.assertEqual(result["name"], "quantum")
        self.assertEqual(result["password"], "secret")
        self.assertEqual(response.status_code, 200)

    def test_admMealsOptions(self):
        response = self.app.get('/api/v1/meals/')
        result = json.loads(response.data)
        self.assertEqual(result["message"], "meals")
        self.assertEqual(response.status_code, 200)
        
    def test_admPostMealsOptions(self):
        response = self.app.post('/api/v1/meals/', data = json.dumps(self.data1) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(result["id"], "1")
        self.assertEqual(result["name"], "Chips")
        self.assertEqual(result["price"], "1000")
        self.assertEqual(response.status_code, 201)
    
    def test_admPutMealsOptions(self):
        response = self.app.put('/api/v1/meals/', data=json.dumps(self.data1), content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result["id"], "1")
        self.assertEqual(result["name"], "Chips")
        self.assertEqual(result["price"], "1000")
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()
