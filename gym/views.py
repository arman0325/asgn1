from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.contrib import messages
from .models import GymUser, GymNow, GymWaiting, Record
from .forms import GymNowForm, GymWaitForm, UploadFileForm
import os, csv
from datetime import datetime
from django.contrib.auth.models import auth, User
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
from gym.functions.functions import handle_uploaded_file

# Create your views here.

#it is the max number of gym room user that will reset in server restart
#can call setMaxUser to modify it
maxNum = 8

def handle_not_found(request, exception):
	return render(request,'404.html')



def index(request):
	return render(request, 'gym/index.html')

#export the csv of the GymUser
def exportGymUser(request):
	response = HttpResponse(content_type='text/csv')

	writer = csv.writer(response)
	writer.writerow(['ID','Name','User Type'])
	for user in GymUser.objects.all().values_list('id','name','userType'):
		writer.writerow(user)

	response['Content-Disposition'] = 'attachment; filename="GymUser.csv"'
	return response

# show the all users
def list(request):
	users = GymUser.objects.all()
	return render(request, 'gym/list.html',
							{'users':users,
							'admin':admin
							})

#Remove the user in waiting list
def importRemove(request):
	request.encoding='utf-8'
	if 'userId' in request.GET and request.GET['userId']:
		id = request.GET['userId']
		GymWaiting.objects.filter(userId=id).delete()
		messages.success(request,"Action successful")
	else:
		messages.success(request,"Action unsuccessful")
	return redirect('/gym/admit/admitGym')

# show sll users currently in the gym

def viewCurrentUsers(request):

	global admin
	if request.user.is_authenticated:
		admin=True
	else:
		admin=False
	users = GymNow.objects.all().order_by('entryTime')
	waitUsers = GymWaiting.objects.all().order_by('waitTime')
	return render(request, 'gym/ViewCurrentUsers.html',
							{'users':users, 
							'waitUsers':waitUsers,
							'admin':admin,
							'max':maxNum
							})

@login_required
def addForm(request):
	new_user = None
	number = GymNow.objects.all().count()
	#return the form type
	if number < maxNum:
		gym_form = GymNowForm()
	else:
		gym_form = GymWaitForm()

	# get the POST data and action
	# gym room is not full 
	if request.method == 'POST' and number < maxNum:
		id = request.POST
		gym_form = GymNowForm(data=request.POST)
		if gym_form.is_valid():
			if not GymNow.objects.filter(userId = id['userId']).exists():
				new_user = gym_form.save(commit=False)
				new_user.save()
				return redirect('/gym/admit/admitGym')
			else:
				return HttpResponse("error")

	# gym room is full add to waiting list
	elif request.method =='POST' and number >= maxNum:
		id = request.POST
		gym_form = GymWaitForm(data=request.POST)
		if gym_form.is_valid():
			# NowExists and WaitExists is using to check the user not in the list that cannot be repeat
			NowExists = GymNow.objects.filter(userId = id['userId']).exists()
			WaitExists = GymWaiting.objects.filter(userId = id['userId']).exists()
			if not NowExists and not WaitExists:
				new_user = gym_form.save(commit=False)
				new_user.save()
				return redirect('/gym/admit/admitGym')
			else:
				return HttpResponse("error")
	return render(request, 'gym/insertForm.html',
							{'gym_form' : gym_form})

@login_required
# waiting list user add to gymNow
def addGym(request):  
	number = GymNow.objects.all().count()
	request.encoding='utf-8'
	if 'userId' in request.GET and request.GET['userId'] and number < maxNum:
		id = request.GET['userId']
		user = GymUser.objects.get(pk=id) #find the user data in GymUser to create in next line
		new_user = GymNow.objects.create(userId=user) # add to gymNow
		GymWaiting.objects.filter(userId=id).delete() # delete from gymWait
		# call the js to alert the message
		messages.success(request,"Action successful")
	else:
		# call the js to alert the message
		messages.success(request,"Gym room is full. Action unsuccessful")
	return redirect('/gym/admit/admitGym')
	
# set the max number of user
@login_required
def SetMaxUsers(request):
	request.encoding='utf-8'
	if 'maxNo' in request.GET and request.GET['maxNo']:
		# global the maxNum to update it
		global maxNum
		maxNum = int(request.GET['maxNo'])
	return render(request, 'gym/setMax.html',
							{'admin':admin,
							'maxNum':maxNum
							})

def userLogin(request):
	if request.method=="POST":
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(request, username=username, password=password)
		if user is not None:

			login(request, user)
			return redirect('/gym/admit/admitGym')
		else:
			return redirect('/gym')
	else:

		return render(request, 'gym/login.html')

def easyLogin(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(request, username=username, password=password)
	if user is not None:
		global admin
		admin = True

		login(request, user)
		return redirect('/gym/admit/admitGym')
	else:
		return redirect('/gym')

def Logout(request):
	auth.logout(request)
	return redirect('/gym')

@login_required
def LeaveGym(request):
	request.encoding='utf-8'
	if 'userId' in request.GET and request.GET['userId']:
		id = request.GET['userId']
		user = GymUser.objects.get(pk=id) #get the user data
		time= GymNow.objects.get(userId=id) #get data from GymNow
		new_user = Record.objects.create(userId=user, entryTime=time.entryTime)
		new_user.save() #save to Record
		GymNow.objects.filter(userId=id).delete() #delete the object
		# call the js to alert the message
		messages.success(request,"Action successful")
	else:
		# call the js to alert the message
		messages.success(request,"Action unsuccessful")
	return redirect('/gym/admit/admitGym')

@login_required
def upload(request):
	form = UploadFileForm()
	if request.method=="POST":
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['file'])
			response = HttpResponse()
			try:
				with open('gym/static/GymUser.csv', newline='') as csvfile:
					rows = csv.reader(csvfile)
					for row in rows:
						try:
							userID, userName = row[0], row[1]
							if GymUser.objects.filter(id=row[0]).exists():
								response.write("{} <span>User exists</span><br>".format(row[0]))
								continue
							else:
								typeUser = 'S' if len(userID) == 8 else 'E'
								print(userID, userName, typeUser)
								newUser = GymUser(id=userID, name=userName, userType=typeUser)
								newUser.save()
								response.write("<span style='color:red'>{} added</span><br>".format(newUser))
						except:
							print("error")
				return response
			except:
				response.write("null data")
				return response

		else:
			form = UploadFileForm()
	return render(request, 'gym/upload.html',{'form':form, 'admin':admin})
