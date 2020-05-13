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



