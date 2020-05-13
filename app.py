from flask import Flask, jsonify 

from resources.users import users
from resources.courses import courses
from resources.milestones import milestones
from resources.enrollments import enrollments
from resources.submissions import submissions

import models 
from flask_cors import CORS
from flask_login import LoginManager


DEBUG=True 
PORT=8000

app = Flask(__name__)

app.secret_key = "Wake up, Neo..."
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	try:
		print("loading the following user")
		user = models.User.get_by_id(user_id)
		return user 
	except models.DoesNotExist:
		return None

CORS(users, origins=['http://localhost:3000'], supports_credentials=True)
CORS(courses, origins=['http://localhost3000'], supports_credentials=True)
CORS(milestones, origins=['http://localhost3000'], supports_credentials=True)
CORS(enrollments, origins=['http://localhost3000'], supports_credentials=True)
CORS(submissions, origins=['http://localhost3000'], supports_credentials=True)

app.register_blueprint(users, url_prefix='/api/v1/users/')
app.register_blueprint(courses, url_prefix='/api/v1/courses/')
app.register_blueprint(milestones, url_prefix='/api/v1/milestones/')
app.register_blueprint(enrollments, url_prefix='/api/v1/enrollments/')
app.register_blueprint(submissions, url_prefix='/api/v1/submissions/')


@app.route('/json-test')
def testjson():
	return jsonify(['matthew', 'mark', 'luke', 'john'])


if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)

	