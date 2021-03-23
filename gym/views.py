import csv
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from .models import GymUser, GymNow, GymWaiting, Record
from .forms import GymNowForm, GymWaitForm
import os
from datetime import datetime
from django.contrib import messages
# Create your views here.

#it is the max number of gym room user
maxNum = 8

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
def index(request):
	users = GymUser.objects.all()
	return render(request, 'gym/index.html',{'users':users})

#import the user to GymUser
def importNew(request):
	response = HttpResponse()
	try:
		with open('GymUser.csv', newline='') as csvfile:
			rows = csv.reader(csvfile)
			for row in rows:
				response.write(row)
		return response
	except:
		response.write("null data")
		return response

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
	users = GymNow.objects.all().order_by('entryTime')
	waitUsers = GymWaiting.objects.all().order_by('waitTime')
	admin = False
	return render(request, 'gym/ViewCurrentUsers.html',
							{'users':users, 
							'waitUsers':waitUsers,
							'admin':admin,
							'max':maxNum
							})

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
			if not GymNow.objects.filter(userId = id['userId']).exists():
				if not GymWaiting.objects.filter(userId = id['userId']).exists():
					new_user = gym_form.save(commit=False)
					new_user.save()
					return redirect('/gym/admit/admitGym')
				else:
					return HttpResponse("error")
			else:
				return HttpResponse("error")
	return render(request, 'gym/insertForm.html',
							{'gym_form' : gym_form})

# waiting list user add to gymNow
def addGym(request):  
	number = GymNow.objects.all().count()
	request.encoding='utf-8'
	if 'userId' in request.GET and request.GET['userId'] and number < maxNum:
		id = request.GET['userId']
		user = GymUser.objects.get(pk=id)
		new_user = GymNow.objects.create(userId=user) # add to gymNow
		GymWaiting.objects.filter(userId=id).delete() # delete from gymWait
		messages.success(request,"Action successful")

	else:
		messages.success(request,"Gym room is full. Action unsuccessful")
	return redirect('/gym/admit/admitGym')
	
# set the max number of user
def SetMaxUsers(request):
	request.encoding='utf-8'
	if 'maxNo' in request.GET and request.GET['maxNo']:

		global maxNum
		maxNum = int(request.GET['maxNo'])
	return render(request, 'gym/setMax.html')

def AdmitUser(request):
	users = GymNow.objects.all().order_by('entryTime')
	waitUsers = GymWaiting.objects.all().order_by('waitTime')
	admin = True
	return render(request, 'gym/ViewCurrentUsers.html',
							{'users':users, 
							'waitUsers':waitUsers,
							'admin':admin,
							'max':maxNum
							})

def LeaveGym(request):
	request.encoding='utf-8'
	if 'userId' in request.GET and request.GET['userId']:
		id = request.GET['userId']
		user = GymUser.objects.get(pk=id) #get the user data
		time= GymNow.objects.get(userId=id) #get data from GymNow
		new_user = Record.objects.create(userId=user, entryTime=time.entryTime)
		new_user.save() #save to Record
		GymNow.objects.filter(userId=id).delete() #delete the object
		messages.success(request,"Action successful")
	else:
		messages.success(request,"Action unsuccessful")
	return redirect('/gym/admit/admitGym')

