import models 
from flask import Blueprint


courses = Blueprint('courses', 'courses')

@courses.route('/', methods=['GET'])
def courses_test():
	return "courses resource working"
