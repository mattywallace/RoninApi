import models 
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required


milestones = Blueprint('milestones', 'milestones')

@milestones.route('/', methods=['GET'])
def milestones_test():
	return "milestones resource working"

@milestones.route('/<course_id>', methods=['POST'])
@login_required
def create_milestone(course_id):
	payload = request.get_json()
	print(payload)
	course = models.Course.get_by_id(course_id)
	new_milestone = models.Milestone.create(
		course_from=course_id,
		prompt=payload['prompt'],
		resources=payload['resources'],
		answer=payload['answer']
	)
	new_milestone_dict = model_to_dict(new_milestone)
	print('here is the new new_milestone_dict')
	print(new_milestone_dict)
	new_milestone_dict['course_from']['administrator'].pop('password')
	return jsonify(
		data=new_milestone_dict,
		message=f"A new milestone has been adde to course id {course.course_name}",
		status=201
	),201 