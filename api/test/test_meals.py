""" Meals endpoints test cases"""
import unittest
import json

from app import create_app
from app.models import db
from instance.config import config


class TestMeal(unittest.TestCase):
    """
    Meal Test class to test create,get,update and delete endpoints.
    """

    def setUp(self):
        """ Set up test Variables"""
        self.app = create_app(config["testing"])
        # initialize the test client
        self.client = self.app.test_client
        self.userdata = {
            "username": "admin",
            "email": "admin@andela.ke",
            "password": "admin123",
            "address":"kitale 12"
            }

        self.data = {"meal_name": "Chips", "price":1000}
        self.data1 = {"meal_name": "Ugali", "price":200}

        with self.app.app_context():
            """ create all tables """
            db.session.close()
            db.drop_all()
            db.create_all()

        self.client().post("api/v2/auth/signup", data=json.dumps(self.userdata),
                           content_type='application/json')
        login = self.client().post('/api/v2/auth/login', data=json.dumps(self.userdata),
                                   content_type='application/json')
        self.token = json.loads(login.data.decode()).get('token')

    def test_get_meals(self):
        """ Test get all meals endpoint"""
        res = self.client().get('/api/v2/meals',
                                headers=dict(Authorization="Bearer " + self.token))
        self.assertEqual(res.status_code, 200)

    def test_create_meals(self):
        """ Test the create meals endpoint"""
        res = self.client().post('/api/v2/meals',
                                 data=json.dumps(self.data),
                                 content_type="application/json",
                                 headers=dict(Authorization="Bearer " + self.token))
        self.assertEqual(res.status_code, 200)

    def test_get_meal_by_id(self):
        """ Test get meal by id endpoint"""
        self.client().post("/api/v2/meals",
                           data=json.dumps(self.data),
                           content_type="application/json",
                           headers=dict(Authorization="Bearer " + self.token))
        res2 = self.client().get('/api/v2/meals/1',
                                 content_type="application/json",
                                 headers=dict(Authorization="Bearer " + self.token))
        self.assertEqual(res2.status_code, 200)

    def test_meal_update(self):
        """Test the meal update endpoint"""
        self.client().post('/api/v2/meals',
                           data=json.dumps(self.data),
                           content_type="application/json",
                           headers=dict(Authorization="Bearer " + self.token))
        res = self.client().put('/api/v2/meals/1',
                                data=json.dumps(self.data1),
                                content_type="application/json",
                                headers=dict(Authorization="Bearer " + self.token))
        self.assertEqual(res.status_code, 200)

    def test_meal_delete(self):
        """"Test the delete meal endpoint"""
        self.client().post('/api/v2/meals',
                           data=json.dumps(self.data),
                           content_type="application/json",
                           headers=dict(Authorization="Bearer " + self.token))
        res = self.client().delete('/api/v2/meals/1',
                                   data=json.dumps(self.data),
                                   content_type="application/json",
                                   headers=dict(Authorization="Bearer " + self.token))
        self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
