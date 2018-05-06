from flask import json, request
from flask_restful import Resource, reqparse
from app.models import db, Menu, Meal, User
from flask_jwt_extended import (
                                JWTManager, 
                                jwt_required, 
                                create_access_token,
                                get_jwt_identity)
from app.views.auth.validate import (
                                     require_admin, 
                                     space_stripper,
                                     name_validator, 
                                     num_check)


class MenuOptions(Resource):
    """
    Update,Delete,PUT and migrate
    """

    @jwt_required
    def get(self, id):
        """
        Method gets a menu by id.
        """
        current_user = User.query.filter_by(email=get_jwt_identity()).first()
        menu = Menu.query.filter_by(id=id).first()

        if menu is None:
            return {"status": "Failed!!",
                    "message": "Enter a valid menu id"}, 404

        if menu.user_id == current_user.id:
            response = menu.json_dump()
            return response

        return {"status": "Failed!",
                "message": "Meal does not exist."}, 404

    @jwt_required
    @require_admin
    def put(self, id):
        """
        Method updates menu.
        """
        json_data = request.get_json(force=True)
        menu = Menu.query.filter_by(id=id).first()
        current_user = User.query.filter_by(email=get_jwt_identity()).first()
        meal = Meal.query.filter_by(id=json_data['meal_id']).first()

        if 'meal_id' not in json_data or 'menu_cartegory' not in json_data:
            return {"status": "Failed!",
                    "message": "Enter a meal_id and menu_cartegory."}, 406

        if menu is None:
            return {"status": "Failed!!",
                    "message": "Please enter a valid meal id"}

        if meal is None:
            return {"status": "Failed!!",
                    "message": "Please enter a valid meal id"}

        if not num_check(json_data['meal_id']):
            return {"status": "Failed!",
                    "message": "Meal id must be an integer"}, 406

        if json_data['menu_cartegory'] == '' or json_data['meal_id'] == '':
            return {"status": "Failed!!",
                    "message": "lease enter a valid  menu Details"}
        if meal.user_id == current_user.id:
            if menu.user_id == current_user.id:
                menu.meal_id = json_data['meal_id']
                menu.meal_item = space_stripper(json_data['menu_cartegory'])
                db.session.commit()
                response = menu.json_dump()
                return{"status": "success", "data": response}, 200
            return {"message": "Item does not exist!"}, 404
        return {"message": "Meal does not exist!"}, 404

    @jwt_required
    @require_admin
    def delete(self, id):
        """
         Method deletes a menu by id.
        """
        json_data = request.get_json(force=True)
        menu = Menu.query.filter_by(id=id).first()
        current_user = User.query.filter_by(email=get_jwt_identity()).first()
        if menu is None:
            return {"status": "Failed!!",
                    "message": "Please enter a valid meal id"}
        if menu.user_id == current_user.id:
            Menu.query.filter_by(id=id).delete()
            db.session.commit()
            response = json.loads(json.dumps(json_data))
            return {"status": "deleted!", "message": response}, 200
        return {"message": "Meal does not exist."}, 404


class MenuList(Resource):
    """
    MenuList resource that has a get and post method.
    """
    @jwt_required
    def get(self):
        """
        Method to get all menus.
        """
        current_user = User.query.filter_by(email=get_jwt_identity()).first()
        menus = Menu.query.filter_by(user_id=current_user.id)
        if menus is None:
            return{"message": "You do not have menus at the moment."}, 404
        response = [menu.json_dump() for menu in menus]
        return {"status": "success", "message": response}, 200

    @jwt_required
    @require_admin
    def post(self):
        """
         Method creates a menu and add meals to the Item
        """
        json_data = request.get_json(force=True)
        
        if 'meal_id'not in json_data or 'menu_cartegory' not in json_data:
            return {"status": "Failed!",
                    "Message": "Please a valid provide a meal_id and menu_cartegory in [Breakfast,Beverages,Lunch,,Super] to add to the menu."}

        menu_item = json_data['menu_cartegory']
        meal_id = json_data['meal_id']
        meal = Meal.query.filter_by(id=meal_id).first()
        if space_stripper(menu_item) == '':
            return {"status": "Failed",
                    "message": "Please enter a valid menu item"}, 406
        if meal_id == '':
            return {"status": "Failed",
                    "message": "Please enter a valid meal id"}, 406
        if meal is None:
            return {"status": "Failed!!",
                    "message": "Please enter a valid meal id"}
        current_user = User.query.filter_by(email=get_jwt_identity()).first()
        user_id = current_user.id
        if meal.user_id == current_user.id:
            menu = Menu(meal_id=meal_id, menu_item=menu_item, user_id=user_id)
            menu.save()
            response = json.loads(json.dumps(menu.json_dump()))
            return {"status": "success", "data": response}, 201
        return {"message": "Meal does not exist"}, 404
