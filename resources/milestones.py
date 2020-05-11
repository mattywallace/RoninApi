import models 
from flask import Blueprint


milestones = Blueprint('milestones', 'milestones')

@milestones.route('/', methods=['GET'])
def milestones_test():
	return "milestones resource working"

