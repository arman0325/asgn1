from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.contrib import messages
from .models import GymUser, GymNow, GymWaiting, Record, RoomStatus
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
f = open("gym/static/Number.txt","r")
maxNum = int(f.readline())
f.close()
admin=False

loginTime = 3

#404 page handling
def handle_not_found(request, exception):
	return render(request,'404.html')

def index(request):
	global loginTime 
	loginTime = 3
	return render(request, 'gym/index.html',{'admin':admin})

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
	room = RoomStatus.objects.get(roomId=1)
	if request.user.is_authenticated:
		admin=True
		if room.roomStatus=="False":
			clean()
	else:
		admin=False
	users = GymNow.objects.all().order_by('entryTime')
	waitUsers = GymWaiting.objects.all().order_by('waitTime')
	
	return render(request, 'gym/ViewCurrentUsers.html',
							{'users':users, 
							'waitUsers':waitUsers,
							'admin':admin,
							'max':maxNum,
							'status':room.roomStatus,
							'action':room.roomAction
							})

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
		f = open("gym/static/Number.txt","w")
		f.write(str(maxNum))
		f.close()

	return render(request, 'gym/setMax.html',
							{'admin':admin,
							'maxNum':maxNum
							})

def userLogin(request):
	global loginTime
	if loginTime<0:
		return redirect('/gym')
	if request.method=="POST":
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('/gym/admit/admitGym')
		else:
			loginTime -= 1
			print(loginTime)
			return render(request, 'gym/login.html',
							{'Msg':'Username or Password is wrong'})
	else:
		return render(request, 'gym/login.html')

def easyLogin(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(request, username=username, password=password)
	if user is not None:
		global admin 
		admin = True #get the admin attribute after success login
		login(request, user)
		return redirect('/gym/')
	else:
		return redirect('/gym')

def Logout(request):
	auth.logout(request)
	global admin
	admin=False
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

#upload csv to admit user
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

# record page
@login_required
def viewRecord(request,id=None):
	users = Record.objects.all().order_by('entryTime')
	if id != None: # has a designated user
		users = Record.objects.filter(userId=id)

	return render(request, 'gym/record.html',
							{'users':users,
							'admin':admin,
							'id':id
							})

#clean the gym table function
#gym user will record but waiting will not.
def clean():
	users = GymNow.objects.all()
	for x in users:
		new_user = Record.objects.create(userId=x.userId, entryTime=x.entryTime)
		new_user.save()
		GymNow.objects.filter(userId=x.userId).delete()
	users = GymWaiting.objects.all()
	for x in users:
		GymWaiting.objects.filter(userId=x.userId).delete()

#clean button of gym room
@login_required	
def cleanGym(request):
	clean()
	return redirect('/gym/admit/admitGym')

@login_required
def GymStatus(request):
	if request.method == 'POST':
		room = RoomStatus.objects.get(roomId=1)
		status = request.POST['status']
		time = request.POST['time']
		if status=="Cleaning" or status=="Teaching": #clean and teach case
			if time=="":
				return render(request, 'gym/status.html',{'Msg':'*Please select the time'})
			room.roomStatus=False
			room.roomAction=status+" End time:"+time
		elif status=="Close": # close case
			room.roomStatus=False
			room.roomAction=status
		else: # open case
			room.roomStatus=True
			room.roomAction=status
		room.save()
		#return HttpResponse(status)
		return redirect('/gym/admit/admitGym')
	return render(request, 'gym/status.html',{'admin':admin})

#for add gym user and add to waiting list
@login_required
def addPage(request, type=0):
	users = GymUser.objects.all().order_by('id')
	if request.method == 'POST':
		da = request.POST.get('userId').split()
		try:
			if not GymNow.objects.filter(userId = da[0]).exists():
				user = GymUser.objects.get(pk=da[0])
				if type==1: # add to waiting list
					new_user = GymWaiting.objects.create(userId=user)
				else: # add gym user
					new_user = GymNow.objects.create(userId=user)
				new_user.save()
				return redirect('/gym/admit/admitGym')
			else: #if user is existing
				return render(request, 'gym/addForm.html',
								{'users' : users,
								'msg':'The user is exist',
								'admin':admin
								})
		except: # the user is not admitted
			return render(request, 'gym/addForm.html',
								{'users' : users,
								'msg':'The user is not admitted',
								'admin':admin
								})
	else: # normal load on page
		return render(request, 'gym/addForm.html',
							{'users' : users,
							'msg':'',
							'admin':admin
							})
