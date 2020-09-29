from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Subject(models.Model):
	title = models.CharField(max_length=50)
	creator = models.ForeignKey('Person' , on_delete = models.CASCADE , null = True )


	def __str__(self):
		return self.title




class Question(models.Model):
	question = models.TextField(max_length=100)
	o1 = models.TextField(max_length=100)
	o2 = models.TextField(max_length=100)
	o3 = models.TextField(max_length=100)
	o4 = models.TextField(max_length=100)
	correct = models.CharField(max_length=10 )
	subject = models.ForeignKey('Subject' , on_delete = models.CASCADE  )


	def __str__(self):
		return self.question




# Register
class Person(models.Model):
	name = models.CharField(max_length=50)
	email = models.CharField(max_length=50,unique = True)
	username = models.OneToOneField(User,on_delete = models.CASCADE)

	def __str__(self):
		return self.name



# Enrolled Quiz  
class Enrollment(models.Model):
	enrollment = models.CharField(max_length=50)
	person = models.ForeignKey('Person' , on_delete = models.CASCADE , null = True )




# Marks
class Mark(models.Model):
	person = models.ForeignKey('Person' , on_delete = models.CASCADE , null = True )
	enroll = models.ForeignKey('Enrollment' , on_delete = models.CASCADE , null = True )
	marks = models.IntegerField()

