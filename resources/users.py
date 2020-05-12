import models 
from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user



users = Blueprint('users', 'users')

@users.route('/', methods=['GET'])
def users_list():
	result = models.User.select()
	user_dicts = [model_to_dict(user) for user in result]
	print(user_dicts)
	return jsonify({
		'data': user_dicts,
		'message': f"Successfully found {len(user_dicts)} users",
		'status': 200
		}), 200


@users.route('/register', methods=['POST'])
def create_user():
	payload = request.get_json()
	payload['email'] = payload['email'].lower()
	payload['username'] = payload['username'].lower()
	print(payload)
	try:
		models.User.get(models.User.email == payload['email'])
		return jsonify(
			data={},
			message=f"A user with the email {payload['email']} already exists",
			status=401,
		), 401
	except models.DoesNotExist: 
			pw_hash = generate_password_hash(payload['password'])
			new_user = models.User.create(
				firstname=payload['firstname'],
				lastname=payload['lastname'],
				email=payload['email'],
				username=payload['username'],
				password=pw_hash,
				is_admin=payload['is_admin']
			)
	created_user_dict = model_to_dict(new_user)
	print(new_user)
	return jsonify(
		data=user_dict,
		message=f"Successfully registered user {created_user_dict['email']}",
		status=201
		), 201

@users.route('/login', methods=['POST'])
def login():
	payload = request.get_json()
	payload['email'] = payload['email'].lower()
	payload['username'] = payload['username'].lower()
	try:
		user = models.User.get(models.User.email == payload['email'])
		user_dict = model_to_dict(user)
		password_is_good = check_password_hash(user_dict['password'], payload['password'])
		if(password_is_good):
			login_user(user)
			user_dict.pop('password')
			return jsonify(
				data=user_dict,
				message=f"successfully logged in {user_dict['email']}",
				status=200
			), 200 
		else:
			print('Password is no good')			
			return jsonify(
				data={},
				message="Email or password is incorrect",
				status=401
			), 401
	except models.DoesNotExist:
		print('Username already exists')
		return jsonify(
			data={},
			message='Email or Password is incorrect',
			status=401
			), 401 





@users.route('/<id>', methods=['PUT'])
def update_user(id):
	payload =request.get_json()
	update_query = models.User.update(
		email=payload['email'],
		username=payload['username'],
		password=payload['password'],
	).where(models.User.id == id)
	num_of_rows_modified = update_query.execute()
	updated_user = models.User.get_by_id(id)
	updated_user_dict = model_to_dict(updated_user)
	return jsonify(
		data=updated_user_dict,
		message=f"Successfully updated with id",
		status=200
	), 200 



@users.route('/<id>', methods=['DELETE'])
def delete_user(id):
	delete_query = models.User.delete().where(models.User.id == id)
	num_of_rows_deleted = delete_query.execute()
	print(num_of_rows_deleted)
	return jsonify(
		data={},
		message='Successfully deleted {} user with id {}'.format(num_of_rows_deleted, id),
		status=200
	), 200












