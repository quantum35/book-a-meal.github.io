from flask import Flask, request, make_response
from flask_restful import Resource,Api
from flask_jwt import JWT,jwt_required 
from security import authenticate,identity

app = Flask(__name__)
app.secret_key = 'Quantum21345'
api = Api(app)

jwt = JWT(app,  authenticate, identity) #creates endpoint /auth

#initialize out JWT Token that our app _is going to use
database =[]
class login(Resource):
    def post(self):
        data = request.get_json()
        db={
            'username':data['username'],
            'email':data['email'],
            'password':data['password']
        }
        return db,201


class signup(Resource):
    def post(self):
        data = request.get_json()
        db = {'username':data['username'],
                'email':data['email'],
                'password':data['password']
                }
        return db,201
#Admin

class addNewMeal(Resource):
    def post(self):
        data = request.get_json()
        db={
            'meal_id':data['meal_id'],
            'name':data['name'],
            'price':data['price']
        }
        return db,201
class UpdatemealOption(Resource):
    def put(self):
        data11 = request.get_json()
        db ={'meal_id':data11['meal_id'],
              'name':data11['name'],
              'price':data11['price']
            }
        return db,201
class modifyMeal(Resource):
    def put(self):
        data4 = request.get_json()
        db = {
            'name':data4['name'],
            'price':data4['price']
        }
        return db,201

class deleteMealOption(Resource):
    def delete(self):
        data1 = request.get_json()
        db =  {
            'meal_id':data1['meal_id'],
            'name':data1['name'],
            'price':data1['price']
        }
        return db,200
        

class setUpmealDay(Resource):
     def post(self):
        data1 = request.get_json()
        db ={
            'meal_id':data1['meal_id'],
            'name':data1['name'],
            'price':data1['price']
        }
        return db,201
class checkOrdersMadebyUser(Resource):
    def get(self):
        return {'message':'Here are The Orders Made by users'}

class checkTodaysProfit(Resource):
    def get(self):
        return {'message':'Todays Profit is'}
class checkOrderHistoryAdmm(Resource):
    def get(self):
        return {'message':'Here is Your History'}
class checkLogedinAdmins(Resource):
    def get(self):
        return {'message':'Return More Than one Admin Loged In'}
#Customers
class custCheckMenu(Resource):
    def get(self):
        return{'message':'Here is your Menu Of the Day'}
    def post(self):
        data = request.get_json()
        db ={
            'name':data['name'],
            'price':data['price']
        }
        return db,201
class updateOrder(Resource):
     def put(self):
        data12 = request.get_json()
        db = {
            'id':data12['id'],
            'name':data12['name'],
            'price':data12['price']
        }
        return db,201

class checkOrderHistory(Resource):
    def get(self):
        return{'message':'Here is your Order History'}

class getNotification(Resource):
    def get(self):
        return{'message':'You have one New Message'}


api.add_resource(login,'/auth/login')
api.add_resource(signup,'/auth/signup')
api.add_resource(addNewMeal, '/meals/')
api.add_resource(deleteMealOption,'/meals/1')
api.add_resource(UpdatemealOption,'/meals/1')
api.add_resource(setUpmealDay,'/menu/')
api.add_resource(checkOrderHistoryAdmm,'/orders')
api.add_resource(modifyMeal,'/menu/1')
api.add_resource(checkOrdersMadebyUser,'/orders/')
api.add_resource(checkTodaysProfit,'/profit')
api.add_resource(checkLogedinAdmins,'/admin/')
#customer
api.add_resource(custCheckMenu,'/users/menu/')
api.add_resource(checkOrderHistory,'/users/orders')
api.add_resource(updateOrder,'/users/orders/1')
api.add_resource(getNotification,'/users/notification')

if __name__ == '__main__':
    app.run(port=5000, debug=True)    