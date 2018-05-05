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
        data = request.get_json(force=True)
        if 'username' not in data or \
             'email' not in data or 'password' not in data or 'address' not in data:
              return {"status": "Failure",
               "message": "Error Submiting Empty Options"},406
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            if not email_validator(data['email']):
                return {"status":"Failure","message":"Please enter a valid email."}
            if not password_validator(data['password']):
                return {"status":"Failure","data":"Short Password"}
            if not user_name_validator(data['username']):
                return {"status":"Failure","message":"Please use a username without special characters."}
            if not address_validator(data['address']):
                return {'status':"Failure","message":"please enter Correct address"}
            
            new_user = User(username=data['username'],
                            email=data['email'],
                            password=data['password'],
                            address = data['address']
                            )
            new_user.save()
            # response = json.loads(json.dumps(new_user.json_dump()))
            return {"status": "successfully signedup please Login"}, 201
        else:
            return {"status":"Failed!","message":"Email already in use by existing user"}


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

