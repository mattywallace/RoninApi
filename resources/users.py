import models 
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict


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
	print(payload)
	new_user = models.User.create(
		firstname=payload['firstname'],
		lastname=payload['lastname'],
		email=payload['email'],
		username=payload['username'],
		password=payload['password'],
		is_admin=payload['is_admin']
	)
	user_dict = model_to_dict(new_user)
	print(new_user)
	return jsonify(
		data=user_dict,
		message='Successfully registered a user',
		status=201
		), 201




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












