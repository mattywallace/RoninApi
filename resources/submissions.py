import models 
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

submissions = Blueprint('submissions', 'submissions')

@submissions.route('/<user_id>/<milestone_id>', methods=['POST'])
@login_required
def create_submission(user_id, milestone_id):
	payload = request.get_json()
	print(payload)
	new_submission = models.Submission.create(
		milestone_sub=milestone_id,
		student_subbed=user_id,
		content=payload['content'],
		approved=payload['approved']
	)
	new_sub_dict = model_to_dict(new_submission)
	print('this is the the new sub dict', new_sub_dict)
	new_sub_dict['student_subbed'].pop('password')
	new_sub_dict['milestone_sub']['course_from']['administrator'].pop('password')
	return jsonify(
		data=new_sub_dict,
		message=f"User {new_sub_dict['student_subbed']['username']} has successfully created a new submission",
		status=201
	),201 

@submissions.route('/<milestone_id>/<id>', methods=['GET'])
@login_required
def show_submission(milestone_id, id):
	submission = models.Submission.get_by_id(id)
	submission_dict = model_to_dict(submission)
	print('here is the submission dict', submission_dict)
	submission_dict['student_subbed'].pop('password')
	submission_dict['milestone_sub']['course_from']['administrator'].pop('password')
	return jsonify(
		data=submission_dict,
		message=f"Here is the submission from user {submission_dict['student_subbed']['username']} for milestone {milestone_id} in course {submission_dict['milestone_sub']['course_from']['course_name']} ",
		status=200
	), 200

@submissions.route('/<milestone_id>/<id>', methods=['PUT'])
@login_required
def submission_update(milestone_id, id):
	payload = request.get_json()
	update_query = models.Submission.update(	
		approved=payload['approved']
	).where(models.Submission.id == id)
	num_of_rows_modified = update_query.execute()
	submission = models.Submission.get_by_id(id)
	submission_dict = model_to_dict(submission)
	print('here is the updated submission dict', submission_dict)
	submission_dict['student_subbed'].pop('password')
	submission_dict['milestone_sub']['course_from']['administrator'].pop('password')
	return jsonify(
		data=submission_dict,
		message=f"Successfully updated submission {id} from course {submission_dict['milestone_sub']['course_from']['course_name']} submitted by {submission_dict['student_subbed']['username']}",
		status=200
	), 200
