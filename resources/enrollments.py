import models 
from flask import Blueprint


enrollments = Blueprint('enrollments', 'enrollments')

@enrollments.route('/', methods=['GET'])
def enrollments_test():
	return "enrollemtns resource working"
