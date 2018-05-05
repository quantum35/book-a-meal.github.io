from flask import json, request
from flask_restful import Resource,reqparse
from app.models import db, Menu,Meal
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from  app.views.auth.validate import require_admin
class MenuOptions(Resource):
    """
    Update,Delete,PUT and migrate
    """

    @jwt_required
    def get(self, id):
        """
        Method gets a menu by id.
        """
        menu = Menu.query.filter_by(id=id).first()
        if menu is None:
            return {"status":"Failed!!",
            "message":"Menu id does not exist.Please enter a valid menu id"}
        response = menu.json_dump()
        return response
    @jwt_required
    @require_admin
    def put(self, id):
        """
        Method updates menu.
        """
        json_data = request.get_json(force=True)
        menu = Menu.query.filter_by(id=id).first()
        if 'meal_id' not in json_data or 'menu_item' not in json_data:
            return {"status":"Failed!","message":"Please provide a meal_id and menu_item to update."}
        if  menu is None:
            return {"status":"Failed!!",
            "message":"Menu id does not exist.Please enter a valid meal id"}
        meal= Meal.query.filter_by(id=json_data['meal_id']).first()
        if  meal is None:
            return {"status":"Failed!!",
            "message":"Meal id does not exist.Please enter a valid meal id"}
        if json_data['menu_item']== '':
            return {"status":"Failed!!",
            "message":"Menu item can not be empty.Please enter a valid menu item"}
        else:
            if json_data['meal_id']:
                menu.meal_id = json_data['meal_id']
            if json_data['menu_item']:
                menu.menu_item = json_data['menu_item']
            db.session.commit()
            response = menu.json_dump()
            return{"status": "success", "data": response}, 200

    @jwt_required
    @require_admin
    def delete(self, id):
        """
         Method deletes a menu by id.
        """
        json_data = request.get_json(force=True)
        menu= Menu.query.filter_by(id=id).first()
        if  menu is None:
            return {"status":"Failed!!",
            "message":"Menu id does not exist.Please enter a valid meal id"}
        else:
            Menu.query.filter_by(id=id).delete()
            db.session.commit()
            response = json.loads(json.dumps(json_data))
            return {"status": "deleted!", "data": response}, 200


class MenuList(Resource):
    """
    MenuList resource that has a get and post method.
    """
    @jwt_required
    def get(self):
        """
        Method to get all menus.
        """
        menus = Menu.query.all()
        response = [menu.json_dump() for menu in menus]
        return {"status": "success", "data": response}, 200
    @jwt_required
    @require_admin
    def post(self):
        """
         Method creates a menu and add meals to the Item
        """
        json_data = request.get_json(force=True)
        
        if 'meal_id'not in json_data or 'menu_cartegory' not in json_data:
            return {"status":"Failed!",
                    "Message":"Please a valid provide a meal_id and menu_cartegory in [Breakfast,Beverages,Lunch,,Super] to add to the menu."}
       
        # menu_cart = ['Breakfast', 'Beverages', 'Lunch', 'Super']
        # check_cart = [u for u in menu_cart if not u]
        
        # if not check_cart:
        #     return {'status':"Failure", 'message':'Enter {}'.format(menu_cart)}
        
        menu_item = json_data['menu_cartegory']
        meal_id   = json_data['meal_id']
        meal= Meal.query.filter_by(id=meal_id).first()
        if menu_item == '':
            return {"status":"Failed",
            "message":"Meal name can not be empty.Please enter a valid menu item"}
        elif meal_id == '' :
            return {"status":"Failed",
            "message":"Meal id can not be empty.Please enter a valid meal id"}
        if  meal is None:
            return {"status":"Failed!!","message":"Please enter a valid meal id"}
        menu = Menu(meal_id=meal_id,menu_item=menu_item)
        menu.save()
        response = json.loads(json.dumps(menu.json_dump()))
        return {"status": "success", "data": response}, 201
