from peewee import *
import datetime 

DATABASE = SqliteDatabase('ronin.sqlite')

class User(Model):
	firstname = CharField()
	lastname = CharField() 
	email = CharField(unique=True)
	username = CharField(unique=True)
	password = CharField() 
	current_courses = ArrayField(ForiegnKeyField( Course, backref='users'))
	completed_courses = ArrayField(ForiegnKeyField( Course, backref='users'))

	class Meta:
		database = DATABASE

def initialize(): 
	DATABASE.connect()
	DATABASE.create_tables([User], safe=True )
	print('Connected to the DB and created tables if they didnt already exist')
	DATABASE.close()