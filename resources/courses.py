import models 
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required



courses = Blueprint('courses', 'courses')

@courses.route('/', methods=['GET'])
def courses_index():
	result = models.Course.select()
	print(result);
	course_dicts =[model_to_dict(course) for course in result]
	for course_dict in course_dicts:
		course_dict['administrator'].pop('password')
	return jsonify({
		'data': course_dicts,
		'message': f" There are currently {len(course_dicts)} courses in the database.",
		'status': 200
		}), 200 
	
	
@courses.route('/list', methods=['GET'])
@login_required
def user_course_index():
	current_user_course_dicts = [model_to_dict(course) for course in current_user.courses]
	for course_dict in current_user_course_dicts:
		course_dict['administrator'].pop('password')
		print(current_user_course_dicts)
		return jsonify({
			'data': current_user_course_dicts,
			'message': f"There are currently {len(current_user_course_dicts)} courses for the THIS USER",
			'status': 200
			}), 200

@courses.route('/<id>', methods=['GET'])
@login_required
def show_course(id):
	course = models.Course.get_by_id(id)
	course_dict = model_to_dict(course)
	course_dict['administrator'].pop('password')
	return jsonify(
		data=course_dict,
		message=f"Found dog with id {id}",
		status=200
	), 200
	


@courses.route('/create', methods=['POST'])
@login_required
def create_course():
	payload = request.get_json()
	payload['course_name'] = payload['course_name'].lower()
	print(payload)
	try:
		models.Course.get(models.Course.course_name == payload['course_name'])
		return jsonify(
			data={},
			message=f"A course with this title has already been created.",
			status=401,
		), 401
	except models.DoesNotExist:
			new_course = models.Course.create(
				course_name=payload['course_name'],
				course_keywords=payload['course_keywords'],
				administrator=current_user.id,
				description=payload['description'],
				certification=payload['certification']
			)
	new_course_dict = model_to_dict(new_course)
	new_course_dict['administrator'].pop('password')
	return jsonify(
		data=course_dict,
		message=f"User {new_course_dict['adminstrator']} has successfully created a new class called {new_course_dict['course_name']}",
		status=201
	),201 

@courses.route('/<id>', methods=['PUT'])
@login_required
def update_dog(id):
	payload = request.get_json()
	update_query = models.Course.update(
		course_name=payload['course_name'],
		course_keywords=payload['course_keywords'],
		description=payload['description'],
		certification=payload['certification']
	).where(models.Course.id == id)
	num_of_rows_modified = update_query.execute()
	updated_course = models.Course.get_by_id(id)
	updated_course_dict = model_to_dict(updated_course)
	return jsonify(
		data=updated_course_dict,
		message=f"Successfully updated course with id {id}",
		status=200
	), 200

@courses.route('/<id>', methods=['DELETE'])
def delete_course(id):
	delete_query = models.Course.delete().where(models.Course.id == id)
	num_of_rows_deleted = delete_query.execute()
	print(num_of_rows_deleted)
	return jsonify(
		data={},
		message="Successfully deleted {} course with the id {}".format(num_of_rows_deleted, id),
		status=200,
	), 200
	



	