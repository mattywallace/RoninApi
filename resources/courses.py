import models 
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required



courses = Blueprint('courses', 'courses')

@courses.route('/', methods=['GET'])
def courses_index():
	result = models.Course.select()
	course_dicts = []
	for course in result :
		course_dict = model_to_dict(course)
		course_dict['administrator'].pop('password')
		milestones = models.Milestone.select().where(models.Milestone.course_from == course.id )
		course_dict['milestones'] = [model_to_dict(milestone) for milestone in milestones]
		course_dicts.append(course_dict)
	# course_dicts = [model_to_dict(course) for course in result]
	# print(course_dicts)
	# for course_dict in course_dicts:
	# 	course_dict['administrator'].pop('password')
	# 	course_dict['milestones'] = [models_to_dict(milestone) for course in result]
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
		message=f"Found course with id {id}",
		status=200
	), 200
	


@courses.route('/create', methods=['POST'])
def create_course():
	course_keywords = ''
	payload = request.get_json()
	if 'course_keywords' in payload:
		course_keywords = payload['course_keywords']
	payload['course_name'] = payload['course_name'].lower()
	print(payload)
	if current_user.is_admin:
		try:
			print('Here is the denied course ')
			models.Course.get(models.Course.course_name == payload['course_name'])
			return jsonify(
				data={},
				message=f"A course with this title has already been created.",
				status=401,
			), 401
		except models.DoesNotExist:
				new_course = models.Course.create(
					course_name=payload['course_name'],
					course_keywords=course_keywords,
					administrator=current_user.id,
					description=payload['description'],
					certification=payload['certification']
				)
				print('here is the created course')
		new_course_dict = model_to_dict(new_course)
		new_course_dict['administrator'].pop('password')
		new_course_dict['milestones'] = []
		return jsonify(
			data=new_course_dict,
			message=f"User {new_course_dict['administrator']['username']} has successfully created a new class called {new_course_dict['course_name']}",
			status=201
		),201 
	else:
		print('not logged in')
		return jsonify(
			data={
				'error':'403 Forbidden'
			},
			message='You are not authorized to create a course.',
			status=403
		), 403




@courses.route('/<id>', methods=['PUT'])
@login_required
def updated_course(id):
	payload = request.get_json()
	current_course = models.Course.get_by_id(id)
	print(current_course.administrator.id)
	if current_user.id == current_course.administrator.id:
		update_query = models.Course.update(
			course_name=payload['course_name'],
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
	else: 
		return jsonify(
			data={
				'error': 'Forbidden Action'
			},
			message= "You are not authorized to edit this course",
			status=403,
		), 403 




@courses.route('/<id>', methods=['DELETE'])
@login_required
def delete_course(id):
	current_course = models.Course.get_by_id(id)
	print(current_course.administrator.id)
	if current_user.id == current_course.administrator.id:
		delete_query = models.Course.delete().where(models.Course.id == id)
		num_of_rows_deleted = delete_query.execute()
		print(num_of_rows_deleted)
		return jsonify(
			data={},
			message="Successfully deleted {} course with the id {}".format(num_of_rows_deleted, id),
			status=200,
		), 200
	else: 
		return jsonify(
			data={
				'error': 'Forbidden Action'
			},
			message= "You are not authorized to delete this course",
			status=403,
		), 403 




	