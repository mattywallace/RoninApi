from flask import Flask, jsonify 

from resources.users import users
from resources.courses import courses
from resources.milestones import milestones
from resources.enrollments import enrollments



import models 
DEBUG=True 
PORT=8000

app = Flask(__name__)

app.register_blueprint(users, url_prefix='/api/v1/users/')
app.register_blueprint(courses, url_prefix='/api/v1/courses/')
app.register_blueprint(milestones, url_prefix='/api/v1/milestones/')
app.register_blueprint(enrollments, url_prefix='/api/v1/enrollments/')


@app.route('/json-test')
def testjson():
	return jsonify(['matthew', 'mark', 'luke', 'john'])


if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)