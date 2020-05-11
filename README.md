### Ronin API ###


+++++++ MODELS +++++++

Class User():
	
	firstname = CharFeild()

	lastname = CharField() 

	email = CharField(unique=true)
	
	username = CharFeild(unique=true)
	
	password = CharField() 

	is_admin = BooleanField()
	

Class Enrollments():
	
	enrolled_user = ForeignKeyField()

	enrolled_course = ForeignKeyField()


Class Course():
	
	cours_name = CharField(unique=True)
	
	course_keyworkds = CharField() 
	
	administrator = ForeignKeyField()
	
	descrption = TextField()
	
	Certification = BooleanField()


Class Submission():
	
	milestone_sub = ForiegnKeyField( Mileston, backref='submissions')

	student_sub = ForiegnKeyField( Mileston, backref='submissions')

	answer = CharField() --upload with cloudinare 

	approved = BooleanField()


Class Milestone():

	course = ForiegnKeyField( Course, backref=' milestones')

	prompt = TextField()

	resources = Charfield() -- cloudinare

	answer = Charfield() -- cloudinare 





+++++++ ROUTES +++++++

----- User Routes ----- 
```
POST /api/v1/users/register
	
	Create New User

GET /api/v1/users/<id>

	User Show Page

GET /api/v1/users/logged_in_user
	
	Allows us to use current_user in code

DELETEL /api/v1/users/<id>

	Deletes a user

PUT /api/v1/users/<id>	

	Updates a User Profile 


----- Course Routes ----- 

POST /api/v1/courses

	Creates Course 

GET /api/v1/courses/<id>

	Course Show Route

DELETE /api/v1/courses/<id>

	Deletes A Course

PUT /api/v1/courses/<id>

	Updates Course Information

GET /api/v1/courses

	Course Index Page 

 ----- Milestone Routes ----- 

POST /api/v1/milestones/

	Creates Milestone

DELETE /api/v1/milestones/<id>

	Deletes a Milestone

PUT /api/v1/milestones/<id>

	Updates Milestone Information

GET /api/v1/milestones/<id>

	Shows A Milestone

--- Submission Route -----

POST /api/v1/submissions/

	create route for submissions

Get /api/v1/submissions/<id>
	
	Shows the submissions
```