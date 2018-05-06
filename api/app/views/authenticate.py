from flask import json, request
from flask_restful import Resource
from app.models import db, User
from app.views.auth.validate import (email_validator,
                                     password_validator,
                                     user_name_validator,
                                     address_validator, 
                                     space_stripper)
from flask_jwt_extended import (
    JWTManager, jwt_required,
    create_access_token,
    get_jwt_identity
)
 

class Signup(Resource):
    """
    Signup for New Users so that they can Make Orders
    """
    
    def post(self):
        """Sigup Funtion with Regex to check for valid inputs"""
        json_data = request.get_json(force=True)
        if 'username' not in json_data or \
            'email' not in json_data or 'password' not in json_data  or \
            'address' not in json_data:
              return {"status": "Failure",
                      "message": "Enter valid signup Data"},406

        user = User.query.filter_by(email=json_data['email']).first()
        if not user:
            if not email_validator(json_data['email']):
                return {"status":"Failure",
                        "message":"Please enter a valid email."}
            if not password_validator(json_data['password']):
                return {"status":"Failure",
                        "message":"Password entered is too short password"}
            if not user_name_validator(json_data['username']):
                return {"status":"Failure",
                        "message":"Enter username without special characters."}
            if not address_validator(json_data['address']):
                return{"status":"Failure", 
                       "message":"Enter a Valid Address"}

            new_user = User(username=json_data['username'],
                            email=json_data['email'],
                            password=json_data['password'],
                            address = json_data['address']
                            )
            new_user.save()
            response = json.loads(json.dumps(new_user.json_dump()))
            return {"status": "success",
                    'message':'You registered successfully.'}, 201
        else:
            return {"status":"Failed!",
                    "message":"Email already exist try another Email"},302


class Login(Resource):
    """
    Login for Registerd Users and Generate Access Tokens
    """

    def post(self):
        """Login Function"""
        data = request.get_json(force=True)
        if 'email' not in data or 'password' not in data:
              return {"status": "Failure",
               "message": "Enter , email and password"},406
        if not email_validator(data['email']):
            return {"status":"Failure",
                    "message":"Please enter a valid email"},406

        user = User.query.filter_by(email=data['email']).first()
        if user and user.password_is_valid(data['password']):
            # response = json.loads(json.dumps(user.json_dump()))
            access_token = create_access_token(identity=data['email'])
            return {"status": "successful", "token":access_token, 
                    'message':'Login successful.'}, 200
        return {"message":"Wrong Password or email"},401

