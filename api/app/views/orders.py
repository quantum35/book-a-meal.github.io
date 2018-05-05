from flask import json, request
from flask_restful import Resource
from app.models import db, Order,Menu,Meal,User
from app.views.auth.validate import mealname_and__menuitem_validator
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from app.views.auth.validate import require_admin

class Orders(Resource):
    """
    Order Resource with GET, POST, PUT and DELETE methods
    """
    
    @jwt_required
    def get(self, id):
        """
        Method gets a order by id.
        """
        order = Order.query.filter_by(id=id).first()
        if order is None:
            return {"status":"Failed!!",
            "message":"Order id does not exist.Please enter a valid order id"}
        response = order.json_dump()
        return response
    @jwt_required
    def put(self, id):
        """
        Method updates order.
        """
        json_data = request.get_json(force=True)
        order = Order.query.filter_by(id=id).first()
        if  order is None:
            return {"status":"Failed!!",
            "message":"Order id does not exist.Please enter a valid order id"}
        if 'user_id' not in json_data or \
             'item_id' not in json_data or 'quantity' not in json_data:
              return {"status": "Failed!",
               "message": "Please supply user id, item id and quantity"},406
        item= Menu.query.filter_by(id=json_data['item_id']).first()
        if  item is None:
            return {"status":"Failed!!",
            "message":"Item id does not exist.Please enter a valid Item id"}
        user = User.query.filter_by(id=json_data['user_id']).first()
        if  user is None:
            return {"status":"Failed!!",
            "message":"User id does not exist.Please enter a valid User id"}
        else:
            order.user_id = json_data['user_id']
            order.item_id = json_data['item_id']
            order.quantity = json_data['quantity']
            db.session.commit()
            response = order.json_dump()
            return{"status": "success", "data": response}, 200

    @jwt_required
    def delete(self, id):
        """
         Method deletes a order by id.
        """
        json_data = request.get_json(force=True)
        order= Order.query.filter_by(id=id).first()
        if  order is None:
            return {"status":"Failed!!",
            "message":"Order id does not exist.Please enter a valid order id"}
        else:
            Order.query.filter_by(id=id).delete()
            db.session.commit()
            response = json.loads(json.dumps(json_data))
            return {"status": "deleted!", "data": response}, 200


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
        orders = Order.query.all()
        response = [order.json_dump() for order in orders]
        return {"status": "success", "message": response}, 200
    @jwt_required
    def post(self):
        """
         Method creates an order.
        """
        json_data = request.get_json(force=True)
        if 'user_id' not in json_data or \
             'item_id' not in json_data or 'quantity' not in json_data:
              return {"status": "Failed!",
               "message": "Please supply user id, item id and quantity"},406
        item_id = json_data['item_id']
        user_id   = json_data['user_id']
        quantity = json_data['quantity']
        item= Menu.query.filter_by(id=item_id).first()
        user= User.query.filter_by(id=user_id).first()
        if item_id == '':
            return {"status":"Failed",
            "message":"Item id can not be empty.Please enter a valid item id"}
        elif user_id == '' :
            return {"status":"Failed",
            "message":"User id can not be empty.Please enter a valid user id"}
        elif quantity == '' :
            return {"status":"Failed",
            "message":"Quantity can not be empty.Please enter  valid quantity"}
        if  item is None:
            return {"status":"Failed!!",
            "message":"Item id does not exist.Please enter a valid item id"}
        if  user is None:
            return {"status":"Failed!!",
            "message":"User id does not exist.Please enter a valid user id"}
        else:
            order = Order(user_id=user_id,item_id=item_id,quantity=quantity)
            order.save()
            response = json.loads(json.dumps(order.json_dump()))
            return {"status": "success", "data": response}, 201