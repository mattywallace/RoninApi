import models 
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required


enrollments = Blueprint('enrollments', 'enrollments')

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

	
