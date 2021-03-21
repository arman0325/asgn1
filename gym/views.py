import csv
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from .models import GymUser, GymNow, GymWaiting
from .forms import GymNowForm, GymWaitForm


from django.contrib import messages
# Create your views here.
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

def importNew(request):
	return HttpResponse("importNew")

def importRemove(request):
	return HttpResponse("importRemove")

# show sll users currently in the gym
def viewCurrentUsers(request):
	users = GymNow.objects.all().order_by('entryTime')
	waitUsers = GymWaiting.objects.all().order_by('waitTime')
	
	new_user = None
	if request.method =='POST':
		gym_form = GymNowForm(data=request.POST)
		if gym_form.is_valid():
			new_user = gym_form.save(commit=False)
			new_user.save()
	else:
		gym_form = GymNowForm()

	return render(request, 'gym/ViewCurrentUsers.html',
							{'users':users, 
							'waitUsers':waitUsers,
							'gym_form' : gym_form
							})

def addForm(request):
	new_user = None
	number = GymNow.objects.all().count()
	if number<8:
		gym_form = GymNowForm()
	else:
		gym_form = GymWaitForm()
	if request.method == 'POST' and number < 8:
		gym_form = GymNowForm(data=request.POST)
		if gym_form.is_valid():
			new_user = gym_form.save(commit=False)
			new_user.save()
			return redirect('/gym/gymroom')
	elif request.method =='POST' and number >= 8:
		gym_form = GymWaitForm(data=request.POST)
		if gym_form.is_valid():
			new_user = gym_form.save(commit=False)
			new_user.save()
			return redirect('/gym/gymroom')

	return render(request, 'gym/insertForm.html',
							{'gym_form' : gym_form})


def addGym(request):  
    number = GymNow.objects.all().count()
    request.encoding='utf-8'
    if 'userId' in request.GET and request.GET['userId'] and number<8:
        id = request.GET['userId']
        user = GymUser.objects.get(pk=id)
        new_user = GymNow.objects.create(userId=user)
        #new_user.save()
        print(user)
        GymWaiting.objects.filter(userId=id).delete()
        messages.success(request,"Action successful")

    else:
        messages.success(request,"Gym room is full. Action unsuccessful")
    return redirect('/gym/gymroom')
	

def SetMaxUsers(request):
	return HttpResponse("SetMaxUsers")

def AdmitUser(request):
	return HttpResponse("AdmitUser")

def LeaveGym(request):
	return HttpResponse("LeaveGym")