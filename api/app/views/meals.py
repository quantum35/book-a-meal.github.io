from flask import json, request
from flask_restful import reqparse,Resource
from app.models import db, Meal,User
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from app.views.auth.validate import require_admin,mealname_and__menuitem_validator


class MealOptions(Resource):
    """
    Enebles Registered Cater/Admin to  add,Update,Delete and get Database
    """
    
    @jwt_required
    @require_admin    
    def get(self, id):
        """
        Method gets a meal by id.
        """
        meal = Meal.query.filter_by(id=id).first()
        if meal is None:
            return {"status":"Failed!!",
            "message":"Meal id does not exist.Please enter a valid meal id"}
        
        response = meal.json_dump()
        return response
    @jwt_required
    @require_admin
    def put(self, id):
        """
        Method updates meal.
        """
        json_data = request.get_json(force=True)
        meal_name = json_data['meal_name']
        price = json_data['price']
        meal = Meal.query.filter_by(id=id).first()
        if 'meal_name' not in json_data or 'price' not in json_data:
            return {"status":"Failure","data":"Please provide a meal a name or price."}
        if meal is None:
            return {"status":"Failure",
            "message":"Meal id does not exist.Please enter a valid meal id"}
        if meal_name == '' or not mealname_and__menuitem_validator(json_data['meal_name']) or price == '':
            return {"status":"Failed!!",
            "message":"Meal name can not be empty.Please enter a valid meal details"}
        else:
            meal.meal_name = meal_name
            db.session.commit()
            response = meal.json_dump()
            return{"status": "success", "data": response}, 200
    @jwt_required
    @require_admin
    def delete(self, id):
        """
         Method deletes a meal by id.
        """
        json_data = request.get_json(force=True)
        meal= Meal.query.filter_by(id=id).first()
        if  meal is None:
            return {"status":"Failed!!",
            "message":"Meal id does not exist.Please enter a valid meal id"}
        else:
            Meal.query.filter_by(id=id).delete()
            db.session.commit()
            response = json.loads(json.dumps(json_data))
            return {"status": "deleted!", "data": response}, 200

class MealLists(Resource):
    """
    MealList is for Geting all the meals in the Database
    """
    @jwt_required
    @require_admin    
    def get(self):
        
        """
        Getting Meals Lists
        """
        meals = Meal.query.all()
        response = [meal.json_dump() for meal in meals]
        return {"status": "success", "data": response}, 200
    @jwt_required
    @require_admin
    def post(self):
        """
         Posting Meals
        """
        json_data = request.get_json(force=True)
        meal_name = json_data['meal_name']
        if 'meal_name' not in json_data:
            return {"status":"Failed!","data":"Please provide a meal a name."}
        if meal_name == '':
            return {"status":"Failed",
            "message":"Meal name can not be empty.Please enter a valid meal name"}
        meal = Meal(meal_name=meal_name)
        meal.save()
        response = json.loads(json.dumps(meal.json_dump()))
        return {"status": "success", "data": response}, 201

    
