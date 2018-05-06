'''Validators for user inputs'''
import re
from app.models import User
from functools import wraps
from flask_jwt_extended import (
    get_jwt_identity
)


def space_stripper(data):
    """ Method to remove white space from inputs."""

    striped = "".join(data.split())
    return striped


def bool_transform(data):
    """ Method to transform user input string to boolean for the is_admin column"""

    strng = "".join(data.split())
    if strng == "true":
        return True
    if strng == "false":
        return False
    else:
        return {"message": "Please enter true or false in the admin field"}, 406


def num_check(data):
    """ Method to validate integer inputs"""

    if re.match("^[-+]?[0-9]+$", str(data)):
        return True


def email_validator(email):
    '''validates user provided email'''
    if re.match(
            "^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,4})$",
            email):
        return True
def address_validator(address):
    '''Handles the validation of address'''
    if re.match(
            "^[#.0-9a-zA-Z\s,-]+$",
            address):
        return True

def password_validator(password):
    '''validates user provided password length'''
    if len(password) > 6:
        return True
def user_name_validator(username):
    '''validates user provided username'''
    if re.match("^[a-zA-Z0-9_]*$", username):
        return True


def name_validator(name):
    '''Validates names provided for meals and menus'''

    if re.match("^[a-zA-Z0-9_\s]*$", name):
        return True

def mealname_and__menuitem_validator(name):
    '''Validates names provided for meals and menus'''
    if re.match("^[a-zA-Z0-9_\s]*$", name):
        return True
def boolean_validator(bool):
    if bool == True or bool == False:
        return True

def require_admin(f):
    @wraps(f)
    def decorator(*args,**kwargs):
        current_user =User.query.filter_by(email=get_jwt_identity()).first()
        print(current_user)
        if not current_user.admin:
            return {"status":"Failed!","data":"Only administrators can access these resource."}
        return f(*args, **kwargs)
    return decorator  
def bool_transform(bool):
    if bool == "true":
        return User.is_admin == True
    if bool == "false":
        return User.is_admin == False
    else:
        return {"data":"Please enter true or false in the admin field."}
