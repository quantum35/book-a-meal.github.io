from flask import Flask, request
from flask_restful import Api,Resource

app = Flask(__name__)
api = Api(app)

database = []

class signup(Resource):
    def post(self):
        data = request.get_json(force= True)
        db = {
            "name":data["name"],
            "email":data["email"],
            "password":data["password"]
        }
        database.append(db)
        return db,201
    def get(self):
        return {'data':database}

class login(Resource):
    def post(self):
        data = request.get_json(force= True)
        for db in database:
            if db['name'] == data['name'] and db['password'] == data['password']:
                return db,200
        return {'Message':'Please Sign Up'},404 
#Admin can addnew item,delete,Update
class admMealsOptions(Resource):
    def get(self):
        return database,200
    def post(self):
           data = request.get_json(force= True)
           db = {
               'id':data['id'],
               'name':data['name'],
               'price':data['price']
           }
           database.append(db)
           return db,201
    def put(self):
        data = request.get_json()
        db = next(filter(lambda x:x['id'] == data['id'],database),None)
        if db is None:
            db = {
                'id':data['id'],
                'name':data['name'],
                'price':data['price']
            }
            database.append(db)
        else:
            db.update(data)
        return db,201
    def delete(self):
        data = request.get_json()
        db = list(filter(lambda x:x['id'] != data['id'],database))   
        database.append(db)
        return db,200         

class admMenu(Resource):
    def get(self):
        return database
    def post(self):
        data = request.get_json()
        db = {
            'id':data['id'],
            'name':data['name'],
            'content':data['content']
        }
        database.append(db)
        return db,200

api.add_resource(signup,'/api/v1/auth/signup')
api.add_resource(login,'/api/v1/auth/login')
api.add_resource(admMealsOptions,'/api/v1/meals/')
api.add_resource(admMenu,'/api/v1/menu/')

if __name__ == '__main__':
    app.run(port=5000, debug=True)