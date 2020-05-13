import models 
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required


milestones = Blueprint('milestones', 'milestones')


# this route needs to be changed so that it will only see the 
# milestones form the course_id

@milestones.route('/<course_id>', methods=['GET'])
@login_required
def milestones_index(course_id):
	result = models.Milestone.select()
	print('here is the result' , result)
	course = models.Course.get_by_id(course_id)
	milestone_dicts = [model_to_dict(milestone) for milestone in result]
	return jsonify({
		"data": milestone_dicts,
		"message": f"There are currently {len(milestone_dicts)} milestones in the {course.course_name} course.",
		"status": 200
	}), 200


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

@milestones.route('/<course_id>/<id>', methods=['GET'])
@login_required
def show_milestone(course_id, id):
	milestone = models.Milestone.get_by_id(id)
	milestone_dict = model_to_dict(milestone)
	milestone_dict['course_from']['administrator'].pop('password')
	return jsonify(
		data=milestone_dict,
		message=f"Found milestone with id {id}",
		status=200
	), 200
	


