import models 
from flask import Blueprint


users = Blueprint('users', 'users')

@users.route('/', methods=['GET'])
def users_test():
	return "users resource working"


