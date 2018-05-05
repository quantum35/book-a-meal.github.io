from flask import json, request
from flask_restful import Resource
from app.models import db, User
from app.views.auth.validate import (email_validator,
                            password_validator,
                            user_name_validator,address_validator
                    
)
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
 

class Signup(Resource):
    """
    Signup for New Users so that they can Make Orders
    """
    def post(self):
        json_data = request.get_json(force=True)
        if 'username' not in json_data or \
             'email' not in json_data or 'password' not in json_data or 'is_admin' not in json_data or \
             'address' not in json_data:
              return {"status": "Failure!",
               "message": "Please supply valid signup Data"},406
        user = User.query.filter_by(email=json_data['email']).first()
        if not user:
            if not email_validator(json_data['email']):
                return {"status":"Failure","message":"Please enter a valid email."}
            if not password_validator(json_data['password']):
                return {"status":"Failure","message":"Too short password"}
            if not user_name_validator(json_data['username']):
                return {"status":"Failure","message":"Please use a username without special characters."}
            if not user_name_validator(json_data['is_admin']): 

                return {"status":"Failure","message":"Please use either True or False for the is_admin field."}
            def bool_transform(strng):
                if strng == "true":
                    return True
                if strng == "false":
                    return False
                else:
                    return {"data":"Please enter true or false in the admin field"}
            if not address_validator(json_data['address']):
                return{"status":"Failure", "message":"Enter Valid Address"}

            new_user = User(username=json_data['username'],
                            email=json_data['email'],
                            password=json_data['password'],
                            address = json_data['address']
                            )
            new_user.save()
            response = json.loads(json.dumps(new_user.json_dump()))
            return {"status": "Registered successfully"}, 201
        else:
            return {"status":"Failed!","data":"Email already in use by existing user"}


class Login(Resource):
    """
    Login for Registerd Users and Generate Access Tokens
    """
    def post(self):
        """Login Function"""
        data = request.get_json(force=True)
        if 'email' not in data or 'password' not in data:
              return {"status": "Failure",
               "data": "Supply , email and password"},406
        if not email_validator(data['email']):
            return {"status":"Failure","message":"Please enter a valid email"}

        user = User.query.filter_by(email=data['email']).first()
        if user and user.password_is_valid(data['password']):
            # response = json.loads(json.dumps(user.json_dump()))
            access_token = create_access_token(identity=data['email'])
            return {"message": "successfully Loged in", "token":access_token}, 200
        return {"data":"Wrong Password or username"}

