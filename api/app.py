from flask import Flask, request
from flask_restful import Api,Resource
from flask_jwt import JWT

app = Flask(__name__)
api = Api(app)

tabelUsers = []
tblMeals = []
tblOrders = []
tblMenu = []
tblmenu = []
class Signup(Resource):
    def post(self):
        data = request.get_json(force= True)
        db = {
            "name":data["name"],
            "email":data["email"],
            "password":data["password"],
            'role':data['role']
        }
        tabelUsers.append(db)
        return db,201
    def get(self):
        return {'data':tabelUsers}

class Login(Resource):
    def post(self):
        data = request.get_json(force= True)
        for db in tabelUsers:
            if db['name'] == data['name'] and db['password'] == data['password']:
                return db,200
        return {'Message':'Please Sign Up'},404 
        
#Admin can addnew item,delete,Update
class AdmMealsOptions(Resource):
    def get(self):
        for db in tblMeals:
            if db['role'] != 'admin':
                return {'message':'You should Be admin to view this'}
            return db,200 

    def post(self,id):
           data = request.get_json(force= True)
           db = {
               'id':id,
               'name':data['name'],
               'price':data['price'],
               'role':data['role']
           }
           tblMeals.append(db)
           return db,201

    def put(self):
        data = request.get_json()
        db = next(filter(lambda x:x['id'] == data['id'],tblMeals),None)
        if db is None:
            db = {
                'id':data['id'],
                'name':data['name'],
                'price':data['price'],
                'role':data['role']
            }
            tblMeals.append(db)
        else:
            db.update(data)
        return db,201
#Filter returns an objects that is converted to list by the list function
    def delete(self,id):
        data = request.get_json()
        db = list(filter(lambda x:x['id'] != id,tblMeals))   
        tblMeals.append(db)
        return db,200   

class AdmMenu(Resource):
    def get(self):
        return tblMenu

    def post(self):
        data = request.get_json()
        db = {
            'caterer':{
                'id':data['id'],
                'name':data['name'],
                'content':data['content'],
                'price':data['price']
            }
            
        }
        tblMenu.append(db)
        return db,200

    def put(self):
        data = request.get_json()
        db = next(filter(lambda x:x['id'] == data['id'],tblMenu),None)
        if db is None:
            db = {
                'id':data['id'],
                'name':data['name'],
                'content':data['content'],
                'price':data['price']
            }
            tblMenu.append(db)
        else:
            db.update(data)
        return db,201
    def delete(self):
        data = request.get_json()
        db = list(filter(lambda x:x['id'] != data['id'],tblMenu))   
        tblMenu.append(db)
        return db,200  

class AdmCheckOrders(Resource):
    def get(self):
        return tblOrders

    def post(self):
        data = request.get_json()
        db = {
            'id':data['id'],
            'name':data['name'],
            'price':data['price']
        }
        tblOrders.append(db)
        return db,201

    def put(self):
        data = request.get_json()
        db = next(filter(lambda x:x['id'] == data['id'],tabelUsers),None)
        if db is None:
            db = {
                'id':data['id'],
                'name':data['name'],
                'price':data['price']
            }
            tblOrders.append(db)
        else:
            db.update(data)
        return db,201


#Client/Customers Do-> see menu of the day-get 
                       #Select menu Post

class CustCheckMenu(Resource):
    def get(self):
        return tblmenu,200
        
    def post(self,id):
        data = request.get_json()
        db = {
            'customer':{
                'id':id,
                'name':data['name'],
                'content':data['content'],
                'price':data['price']
            }
            
        }
        tblMenu.append(db)
        return db,201


api.add_resource(Signup,'/api/v1/auth/signup')
api.add_resource(Login,'/api/v1/auth/login')
api.add_resource(AdmMealsOptions,'/api/v1/meals/','/api/v1/meals/<int:id>')
api.add_resource(AdmMenu,'/api/v1/menu/')
api.add_resource(AdmCheckOrders,'/api/v1/orders/')
api.add_resource(CustCheckMenu,'/api/v1/user/menu/','/api/v1/user/menu/<int:id>')

if __name__ == '__main__':
    app.run(port=5000, debug=True)