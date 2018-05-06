from flask import json, request
from flask_restful import Resource
from app.models import db, Order, Menu, Meal, User
from app.views.auth.validate import mealname_and__menuitem_validator
from flask_jwt_extended import (
                                JWTManager,
                                jwt_required, 
                                create_access_token,
                                get_jwt_identity
)
from app.views.auth.validate import require_admin, num_check, name_validator


class Orders(Resource):
    """
    Order Resource with GET, POST, PUT and DELETE methods
    """
    
    @jwt_required
    def get(self, id):
        """
        Method gets a order by id.
        """
        current_user = User.query.filter_by(email=get_jwt_identity()).first()
        order = Order.query.filter_by(id=id).first()
        if order is None:
            return {"status": "Failed!!",
                    "message": "Please enter a valid order id"}, 404
        if order.user_id == current_user.id:
            response = order.json_dump()
            return response
        return {"message": "Order does not exist"}, 404

    @jwt_required
    def put(self, id):
        """
        Method updates order.
        """
        json_data = request.get_json(force=True)
        current_user = User.query.filter_by(email=get_jwt_identity()).first()
        item = Menu.query.filter_by(id=json_data['menu_id']).first()
        order = Order.query.filter_by(id=id).first()
        if order is None:
            return {"status": "Failed!!",
                    "message": "Order id does not exist.Please enter a valid order id"}, 404

        if not num_check(json_data['menu_id']) or not num_check(json_data['quantity']):
            return {"status": "Failed!",
                    "meassage": "Meal_id,item_id and quantity must be integers."}, 406

        if item is None:
            return {"status": "Failed!!",
                    "message": "Item id does not exist.Please enter a valid Item id"}, 404
        
        if item.user_id == current_user.id:
            if order.user_id == current_user.id:
                order.item_id = json_data['menu_id']
                order.quantity = json_data['quantity']
                db.session.commit()
                response = order.json_dump()
                return{"status": "success", "data": response}, 200
            return {"message": "Order does not exist"}, 404
        return {"message": "Item does not exist!"}, 404

    @jwt_required
    def delete(self, id):
        """
         Method deletes a order by id.
        """
        json_data = request.get_json(force=True)
        order = Order.query.filter_by(id=id).first()
        current_user = User.query.filter_by(email=get_jwt_identity()).first()
        
        if order is None:
            return {"status": "Failed!!",
                    "message": "Order id does not exist.Please enter a valid order id"}
        
        if order.user_id == current_user.id:
            Order.query.filter_by(id=id).delete()
            db.session.commit()
            response = json.loads(json.dumps(json_data))
            return {"status": "deleted!", "data": response}, 200
        return {"message": "Order does not exist."}, 404


class OrderLists(Resource):
    """
    OrderList resource that has a get and post method.
    """
    @jwt_required
    @require_admin
    def get(self):
        """
        Method to get all orders.
        """
        current_user = User.query.filter_by(email=get_jwt_identity()).first()
        orders = Order.query.filter_by(user_id=current_user.id)
        if orders is None:
            return{"message": "You do not have orders at the moment."}, 404
        response = [order.json_dump() for order in orders]
        return {"status": "success", "message": response}, 200

    @jwt_required
    def post(self):
        """
         Method creates an order.
        """
        json_data = request.get_json(force=True)
        if 'menu_id' not in json_data or 'quantity' not in json_data:
            return {"status": "Failed!",
                    "message": "Please supply menu_id and quantity"}, 406
        if not num_check(json_data['menu_id']) or not num_check(json_data['quantity']):
            return {"status": "Failed!", 
                    "message": "Item and quantity id must be integers"}, 406
        
        item_id = json_data['menu_id']
        quantity = json_data['quantity']
        item = Menu.query.filter_by(id=item_id).first()
        if item_id == '':
            return {"status": "Failed",
                    "message": "Item id can not be empty.Please enter a valid item id"}, 406
        elif quantity == '':
            return {"status": "Failed",
                    "message": "Quantity can not be empty.Please enter  valid quantity"}, 406
        if  item is None:
            return {"status": "Failed!!",
                    "message": "Item id does not exist.Please enter a valid item id"}, 404
            
        current_user = User.query.filter_by(email=get_jwt_identity()).first()
        user_id = current_user.id
        order = Order(user_id=user_id, item_id=item_id, quantity=quantity)
        order.save()
        response = json.loads(json.dumps(order.json_dump()))
        return {"status": "success", "data": response}, 201
