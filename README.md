### Ronin API ###


+++++++ MODELS +++++++

Class User():
	firstname: CharFeild()
	lastname: CharField() 
	username: CharFeild()
	password: CharField() 
	Courses: ArrayField(ForiegnKeyField)

Class Administrator():
	firstname: CharField()
	lastname: CharField()
	username: CharField()
	password: CharField()
	created_Courses: ArrayField(ForiegnKeyField)
	date_creted: 

Class Course():
	cours_name: CharField(unique=True)
	course_keyworkds: CharField() 
	administrator: CharField()
	descrption: TextField()
	Milestones: ArrayField(ForiegnKeyField)
	Certification: BooleanField()

Class Milestone():
	course: ForiegnKeyField()
	prompt: ArrayField(UPLOADEDADMINFILES)
	Answer: ArrayField(UPLOADEDUSERFILES)


+++++++ ROUTES +++++++

----- User Routes ----- 

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


----- Admin Routes ----- 

POST /api/v1/admins/register
	
	Creates a New Admin 

GET /api/v1/admins/<id>

	Admin Show Page 

GET /api/v1/admins/logged_in_admin
	
	Allows current_admin

DELETEL /api/v1/admins/<id>

	Deletes Admin

PUT /api/v1/admins/<id>	

	Updates an Admin Profile 



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

POST /api/v1/milestones

	Creates  Milestone

DELETE /api/v1/milestones/<id>

	Deletes a Milestone

PUT /api/v1/milestones/<id>

	Updates Milestone Information

GET /api/v1/milestones/<id>

	Shows A Milestone
