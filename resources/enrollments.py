import models 
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required


enrollments = Blueprint('enrollments', 'enrollments')



@enrollments.route('/', methods=['GET'])
def enrollments_index():
	result = models.Enrollment.select()
	print('THIS IS THE CURRENT USER', current_user)
	print(result);
	enrollment_dicts =[model_to_dict(enrollment) for enrollment in result]
	for enrollment_dict in enrollment_dicts:
		enrollment_dict['enrolled_user'].pop('password')
	return jsonify({
		'data': enrollment_dicts,
		'message': f" There are currently {len(enrollment_dicts)} enrollments in the database.",
		'status': 200
		}), 200 



@enrollments.route('/<course_id>/<user_id>', methods=['POST'])
@login_required
def create_enrollemnts(course_id, user_id):
	payload = request.get_json()
	print(payload)
	try:
		models.Enrollment.get(models.Enrollment.enrolled_user == user_id)
		return jsonify(
			data={},
			message=f"user is already enrolled in this course",
			status=401,
		), 401
	except models.DoesNotExist:
		new_enrollment = models.Enrollment.create(
			enrolled_user=user_id,
			enrolled_course=course_id 		
		)
	new_enrollment_dict = model_to_dict(new_enrollment)
	print("here is the new enrollment", new_enrollment_dict)
	new_enrollment_dict['enrolled_user'].pop('password')
	return jsonify(
		data=new_enrollment_dict,
		message=f"User {new_enrollment_dict['enrolled_user']['username']} has successfully been enrolled in {new_enrollment_dict['enrolled_course']['course_name']}",
		status=201
	),201 

@enrollments.route('/<id>', methods=['DELETE'])
@login_required
def delete_enrollments(id):
	current_enrollment = models.Enrollment.get_by_id(id)
	print(current_enrollment.enrolled_user)
	if current_user.id == current_enrollment.enrolled_user.id:
		delete_query = models.Enrollment.delete().where(models.Enrollment.id == id)
		num_of_rows_deleted = delete_query.execute()
		print(num_of_rows_deleted)
		return jsonify(
			data={},
			message="Successfully deleted {} enrollment with the id {}".format(num_of_rows_deleted, id),
			status=200,
		), 200
	else: 
		return jsonify(
			data={
				'error': 'Forbidden Action'
			},
			message= "You are not authorized to delete this Enrollment",
			status=403,
		), 403 
	
