import os
from peewee import *
import datetime 
from flask_login import UserMixin
from playhouse.db_url import connect



if 'ON_HEROKU' in os.environ:
	DATABASE = connect(os.environ.get('DATABASE_URL'))

else: 
	DATABASE = SqliteDatabase('ronin.sqlite')

class User(UserMixin, Model):
	firstname = CharField()
	lastname = CharField() 
	email = CharField(unique=True)
	username = CharField(unique=True)
	password = CharField() 
	is_admin = BooleanField()
	class Meta:
		database = DATABASE

class Course(Model):	
	course_name = CharField(unique=True)	
	course_keywords = CharField(null = False) 	
	administrator = ForeignKeyField( User , backref='courses')	
	description = TextField()	
	certification = BooleanField()
	class Meta:
		database = DATABASE


class Enrollment(Model):
	enrolled_user = ForeignKeyField( User , backref='enrollments')
	enrolled_course = ForeignKeyField( Course, backref='enrollments')
	class Meta: 
		database = DATABASE

class Milestone(Model):
	course_from = ForeignKeyField( Course , backref=' milestones')
	prompt = TextField()
	resources = CharField() # cloudinary
	class Meta:
		database = DATABASE

class Submission(Model):	
	milestone_sub = ForeignKeyField( Milestone, backref='submissions')
	student_subbed = ForeignKeyField( User, backref='submissions')
	content = CharField() # cloudinary
	approved = BooleanField()
	class Meta:
		database = DATABASE


def initialize(): 
	DATABASE.connect()
	DATABASE.create_tables([User, Enrollment, Course, Milestone, Submission], safe=True )
	print('Connected to the DB and created tables if they didnt already exist')
	DATABASE.close()