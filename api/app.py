from flask import Flask, request, jsonify
from project.myclasses.user import User
from project.myclasses.caterer import Caterer
from functools import wraps
import jwt

app = Flask(__name__)


def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None

		if 'Authorization' in request.headers:
			token = request.headers['Authorization']

		if not token:
			return jsonify({"message": "Token is missing!"}), 401

		try:
			data = jwt.decode(token, '$%SECRET_KEY@#^@$')
			active = [u for u in User().users if u["user_id"]
                            == data["user_id"]]
			current_user = active[0]
		except:
			return jsonify({"message": "Token is Invalid!"}), 401

		return f(current_user, *args, **kwargs)

	return decorated


@app.route('/api/v1/users', methods=['GET'])
@token_required
def get_users(current_user):
    
	if not current_user['admin']:
		return ('You Dont Have Enough Privileges to View userlist @ {}'.format(current_user['username']))
    
	users = User().show_users()
	return jsonify({"message": users})


@app.route('/api/v1/auth/signup', methods=['POST'])
def signup():
	new_user = User().signup(
		request.json['username'], request.json['password'], request.json['user_id'])
	return jsonify({"user": new_user})


@app.route('/api/v1/auth/login', methods=['POST'])
def login():
	login = User().login(request.json['username'], request.json['password'])
	return jsonify({"message": login})


@app.route('/api/v1/auth/logout', methods=['POST'])
@token_required
def logout_user(current_user):
	logouts = User().logout()
	return jsonify({"message": logouts})


@app.route('/api/v1/meals/', methods=['GET'])
@token_required
def get_all_meals(current_user):
	if not current_user['admin']:
		return 'Only available for Admin!'

	get_meals = Caterer().get_meals()
	return jsonify({"messages": get_meals})


@app.route('/api/v1/meals/', methods=['POST'])
@token_required
def add_meal(current_user):
	if not current_user['admin']:
		return 'Only available for Admin!'

	new_meal = Caterer().post_meal(request.json['meal_id'], request.json['meal_name'],
                                request.json['price'], request.json['category'], request.json['day'])
	return jsonify({"message": new_meal})


@app.route('/api/v1/meals/<mealId>', methods=['PUT'])
@token_required
def edit_meal(current_user, mealId):
	if not current_user['admin']:
		return 'Only available for Admin!'

	new_meal = Caterer().modify_meal(mealId,
                                  request.json['meal_name'], request.json['price'], request.json['category'], request.json['day'])
	return jsonify({"message": new_meal})


@app.route('/api/v1/meals/<mealId>', methods=['DELETE'])
@token_required
def delete_meals(current_user, mealId):
	if not current_user['admin']:
		return 'Only available for Admin!'

	delete_meal = Caterer().delete_ml(mealId)
	return jsonify({"message": delete_meal})


@app.route('/api/v1/menu/', methods=['POST'])
@token_required
def setup_menu(current_user):
	if not current_user['admin']:
		return 'Only available for Admin!'

	post_menu = Caterer().post_menu(request.json['meal_id'], request.json['meal_name'],
                                 request.json['price'], request.json['category'], request.json['day'])
	return jsonify({"messages": post_menu})


@app.route('/api/v1/menu/', methods=['GET'])
@token_required
def menu_getter(current_user):
	if current_user['admin']:
		return 'Only available for users!'

	get_menu = User().get_menu()
	return jsonify({"messages": get_menu})


@app.route('/api/v1/orders', methods=['POST'])
@token_required
def make_orders(current_user):
	if current_user['admin']:
		return 'Only available for users!'

	new_order = User().make_order(request.json['meal_id'], request.json['meal_name'], request.json['price'],
                               request.json['category'], request.json['day'], request.json['quantity'], request.json['username'])
	return jsonify({"messages": new_order})


@app.route('/api/v1/orders/<orderId>', methods=['PUT'])
@token_required
def modify_orders(current_user, orderId):
	if current_user['admin']:
		return 'Only available for users!'

	mod = User().modify_order(orderId, request.json['quantity'])
	return jsonify({"messages": mod})


@app.route('/api/v1/orders/<orderId>', methods=['DELETE'])
@token_required
def delete_orders(current_user, orderId):
	if current_user['admin']:
		return 'Only available for users!'

	# delete = Caterer().remove_order(orderId)
	return jsonify({"messages": 'delete'})


@app.route('/api/v1/orders', methods=['GET'])
@token_required
def get_all_orders(current_user):
	if not current_user['admin']:
		return 'Only available for Admin!'

	get_order = Caterer().get_orders()
	return jsonify({"messages": get_order})


if __name__ == "__main__":
	app.run(debug=True)
