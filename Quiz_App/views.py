from django.shortcuts import render , HttpResponse , redirect
from .models import *
from django.contrib import auth
import random
from django.contrib.auth.views import PasswordChangeForm,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetConfirmView
from Django_Main_App.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
def home(request):
	return render(request , 'home.html')

def dashboard(request):
	if not request.user.is_authenticated:
		return redirect('/')
	if request.user.is_superuser:
		return redirect('/')
	return render(request , 'dashboard.html')

def quiz(request , id):
	if not request.user.is_authenticated:
		return redirect('login')
	if request.user.is_superuser:
		return redirect('login')

	if request.method == 'POST':
		p  = Person.objects.get(username = request.user)
		print(p)
		subject = Subject.objects.get(id=id)
		print(subject)


		# Save To DB => Enrollment
		check = Enrollment.objects.filter(enrollment=subject , person = p)
		if not check:
			new_enrollment = Enrollment(enrollment = subject , person = p)
			new_enrollment.save()
			e = Enrollment.objects.get(enrollment = subject , person=p)
			print(e)
			data = Question.objects.filter(subject=id)
			ques_id = []
			ans = []
			for i in data:
				ques_id.append(i.id)
				ans.append(i.correct)
			user_ans = []
			print(ans)
			print(ques_id)
			for j in range(len(ques_id)):
				user_ans.append(request.POST['q'+str(int(ques_id[j]))])
			print(user_ans)
			c=0
			for x in range(len(ques_id)):
				if user_ans[x]==ans[x]:
					c=c+1

			# Adding Marks To DB=>Marks
			marks_in_percent = (c/len(ques_id))*100

			new_marks = Mark(person = p , enroll = e , marks = int(marks_in_percent))
			new_marks.save()
			print('Your Marks {} %'.format(int(marks_in_percent)))

			# Marks Sending To Email
			s = str(subject.title)
			creator_quiz = str(subject.creator)
			subject = 'Quiz Result'
			message = "\n\nHello {} ,\n\nYou have successfully attempted {} Quiz created by {} and You have scored {} %.\n\nKeep Participating !!! ✌❤😎\n\nThanks for using this website.".format(p.name,s,creator_quiz,marks_in_percent)

			recepient = [p.email]
			send_mail(subject, message, EMAIL_HOST_USER, recepient, fail_silently = False)
			print('Email ok')
			total = 100-int(marks_in_percent)

			return render(request , 'render_result.html',{'marks':marks_in_percent,'total':total})
		else:
			print('ALready attempted')
			return redirect('/submissions')

	return redirect('/all_quiz')



def create_category(request):
	if not request.user.is_authenticated:
		return redirect('login')
	if request.user.is_superuser:
		return redirect('login')
	if request.method == 'POST':
		p  = Person.objects.get(username = request.user)
		new_subject = Subject(title = request.POST['category'] , creator = p)
		new_subject.save()
		print(new_subject.id)
		subject = new_subject.id
		return redirect(add_question,id = subject)
	return render(request,'select_category.html')



def add_question(request , id):
	if request.method == 'POST':

		d = Subject.objects.get(id = id)
		print(d.title)
		print(request.POST['ques'], request.POST['ans1'],request.POST['ans2'],request.POST['ans3'],request.POST['ans4'],request.POST['correct'])
		new_question = Question(question = request.POST['ques'] , o1 = request.POST['ans1'] , o2 = request.POST['ans2'] , o3 = request.POST['ans3'] , o4 = request.POST['ans4'] , correct = request.POST['correct'] , subject = d)
		new_question.save()
		return render(request , 'add_question.html',{'id':id,'title':d.title,'d':d})
	d = Subject.objects.get(id = id)
	print(d.title)
	return render(request,'add_question.html',{'id':id,'title':d.title,'d':d})


def all_quiz(request):
	x = Subject.objects.all()
	return render(request , 'all_quiz.html' , {'x':x})


def single_quiz(request , id):
	s_id = id
	data = Question.objects.filter(subject=id)
	return render(request , 'single_quiz.html' , {'data':data , 's_id':id})


def register(request):
	# x = User.objects.all()
	if request.method == 'POST':
		try:
			username = request.POST['username']
			username = str(username)
			username = "".join(username.split())
			email = request.POST['email']
			print(username,email)
			user = User.objects.filter(email=email)
			usern = User.objects.filter(username=username)
			if len(user)==0 and len(usern)==0:
				raise User.DoesNotExist

			# print(user,email)
			print(request.POST['username'])
			return render(request,'register.html',{"error":"Email or Username already Registered 🥱😴😛"})
		except User.DoesNotExist:
			user = User.objects.create_user(username=request.POST['username'],password=request.POST['password'],email = request.POST['email'])
			new_user = Person(username = user , name = request.POST['name'] ,  email = request.POST['email'] )
			new_user.save()
			print('Done')

			email = request.POST['email']
			subject = 'Account Activation'
			message = "Hello {} ,\nYour account has been successfully created.✔❤✌".format(request.POST['name'])
			recepient = [email]
			send_mail(subject, message, EMAIL_HOST_USER, recepient, fail_silently = False)
			print('Email ok')
			return render(request,'register.html',{"error":"Your account have been Registered 🥱😴😛"})

	else:
		return render(request,'register.html')

def login(request):
	if request.method == 'POST':
		try:
			# Check User in DB
	 		uname = request.POST['username']
	 		pwd = request.POST['password']
	 		User.objects.get(username=uname)
	 		user_authenticate = auth.authenticate(username=uname,password=pwd)
	 		if user_authenticate is not None:
	 			auth.login(request,user_authenticate)
	 			print('Successfully Login')
	 			return redirect('dashboard')
	 		else:
	 			print('Login Failed')
	 			return render(request , 'login.html',{"error":"Invalid Credentials 🤨🙄😏"})
		except:
			try:
				uemail = request.POST['username']
				print(uemail)
				uname = User.objects.get(email = uemail)
				print(uname)
				pwd = request.POST['password']
				print('hii')
				user_authenticate = auth.authenticate(username=uname,password=pwd)
				if user_authenticate is not None:
		 			auth.login(request,user_authenticate)
		 			print('Successfully Login')
		 			return redirect('dashboard')
				else:
		 			print('Login Failed')
	 				return render(request , 'login.html',{"error":"Invalid Credentials 🤨🙄😏"})

			except:
	 			return render(request , 'login.html',{"error":"Invalid Credentials 🤨🙄😏"})

	else:
		return render(request,'login.html')


# Logout
def logout(request):
	auth.logout(request)
	print('Logout')
	return redirect('/login')


def profile(request):
	if not request.user.is_authenticated:
		return redirect('login')
	if request.user.is_superuser:
		return redirect('login')
	return render(request,'profile.html')

# def verification(request  ):
# 	if request.method == 'POST':
# 		return render(request , 'verification.html')
# 	return render(request , 'verification.html')

def created_quiz(request):
	if not request.user.is_authenticated:
		return redirect('login')
	if request.user.is_superuser:
		return redirect('login')
	p  = Person.objects.get(username = request.user)
	x = Subject.objects.filter(creator = p)
	# print(x[0])
	return render(request , 'created_quiz.html' , {'x':x})

def submissions(request):
	if not request.user.is_authenticated:
		return redirect('login')
	if request.user.is_superuser:
		return redirect('login')

	# Get Enrolled Data
	p  = Person.objects.get(username = request.user)
	data = Enrollment.objects.filter(person = p)
	marks = Mark.objects.filter(person = p)
	# questions = Question.objects.filter()
	print(marks)

	return render(request , 'submissions.html',{'data':data,'marks':marks,'x':len(data)})


def final_submit(request , id):
	p  = Person.objects.get(username = request.user)
	x  = Subject.objects.get(id=id)
	title = x.title
	email = p.email
	subject = 'Quiz Creation'
	message = "Hello {} ,\n\nYour quiz named {} has been successfully created.✔\n\nThanks for your contribution ❤".format(p.name,title)
	recepient = [email]
	send_mail(subject, message, EMAIL_HOST_USER, recepient, fail_silently = False)
	print('Email ok')
	return redirect('/all_quiz')

def render_result(request):
	pass



def my_quiz(request):
	if not request.user.is_authenticated:
		return redirect('login')
	if request.user.is_superuser:
		return redirect('login')
	p  = Person.objects.get(username = request.user)
	x =  Subject.objects.filter(creator = p)
	print(x)

	return render(request,'my_quiz.html',{'x':x})

def delete_quiz(request , id ):
	if not request.user.is_authenticated:
		return redirect('login')
	if request.user.is_superuser:
		return redirect('login')
	data = Subject.objects.get(id=id)
	data.delete()
	return redirect('my_quiz')

def all_submissions(request):
	if not request.user.is_authenticated:
		return redirect('login')
	if request.user.is_superuser:
		return redirect('login')
	p  = Person.objects.get(username = request.user)
	x =  Enrollment.objects.filter(person = p)
	for i in x:
		print(i.id)
	return render(request , 'all_submissions.html',{'x':x})
   

def get_answers(request,id):
	if not request.user.is_authenticated:
		return redirect('login')
	if request.user.is_superuser:
		return redirect('login')
	try:
		e  = Enrollment.objects.get(id=id)
		print(e)
		s = Subject.objects.get(title=e.enrollment)
		print(s.id)
		q = Question.objects.filter(subject=s.id)
		print(q)
		return render(request,'get_answers.html',{'x':q})
	except:
		return render(request,'get_answers.html')
		
	# except:
		# return render(request,'error.html')


