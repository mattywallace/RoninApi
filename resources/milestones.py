import models 
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required


milestones = Blueprint('milestones', 'milestones')




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
	course_dict = model_to_dict(course)
	admin_id = course_dict['administrator']['id']
	if current_user.id == admin_id: 
		new_milestone = models.Milestone.create(
			course_from=course_id,
			prompt=payload['prompt'],
			resources=payload['resources'],
		)
		new_milestone_dict = model_to_dict(new_milestone)
		print('here is the new new_milestone_dict')
		print(new_milestone_dict)
		new_milestone_dict['course_from']['administrator'].pop('password')
		return jsonify(
			data=new_milestone_dict,
			message=f"A new milestone has been adde to course id {course.course_name}",
			status=200
		), 200 
	else:
		return jsonify(
			data={
				'error': 'Forbidden Action'
			},
			message="You are not allowed to create a milestone for this course", 
			status=403 
		), 403 


@milestones.route('/<course_id>/<id>', methods=['GET'])
@login_required
def show_milestone(course_id, id):
	milestone = models.Milestone.get_by_id(id)
	milestone_dict = model_to_dict(milestone)
	milestone_dict['course_from']['administrator'].pop('password')
	return jsonify(
		data=milestone_dict,
		message=f"Found milestone with id {id} from course {milestone_dict['course_from']['course_name']}",
		status=200
	), 200


@milestones.route('/<course_id>/<id>', methods=['PUT'])
@login_required
def update_Milestone(course_id, id):
	payload = request.get_json()
	course = models.Course.get_by_id(course_id)
	course_dict = model_to_dict(course)
	admin_id = course_dict['administrator']['id']
	if current_user.id == admin_id :
		update_query = models.Milestone.update(
			prompt=payload['prompt'],
			resources=payload['resources'],
		).where(models.Milestone.id == id)
		num_of_rows_modified = update_query.execute()
		updated_milestone = models.Milestone.get_by_id(id)
		updated_milestone_dict = model_to_dict(updated_milestone)
		updated_milestone_dict['course_from']['administrator'].pop('password')
		return jsonify(
			data=updated_milestone_dict,
			message=f"Successfully updated milestone {id} from course {updated_milestone_dict['course_from']['course_name']}",
			status=200
		), 200
	else: 
		return jsonify(
			data={
				'error': 'Forbidden Action'
			},
			message="You are not allowed to update this milestone", 
			status=403 
		), 403 

	
@milestones.route('/<course_id>/<id>', methods=['DELETE'])
@login_required
def delete_milestone(course_id, id):
	course = models.Course.get_by_id(course_id)
	course_dict = model_to_dict(course)
	admin_id = course_dict['administrator']['id']
	if current_user.id == admin_id:
		delete_query = models.Milestone.delete().where(models.Milestone.id == id)
		num_of_rows_deleted = delete_query.execute()
		print(num_of_rows_deleted)
		return jsonify(
			data={},
			message="Successfully deleted {} course(s) with the id {}".format(num_of_rows_deleted, id),
			status=200,
		), 200
	else: 
		return jsonify(
			data={
				'error': 'Forbidden Action'
			},
			message="You are not allowed to delete this this milestone", 
			status=403 
		), 403 







