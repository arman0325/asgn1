import csv
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from .models import GymUser, GymNow, GymWaiting
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
	return render(request, 'gym/ViewCurrentUsers.html',
							{'users':users, 
							'waitUsers':waitUsers})

def addGym(request):  
    request.encoding='utf-8'
    if 'userId' in request.GET and request.GET['userId']:
        message = '你搜索的内容为: ' + request.GET['userId']
        
        addGymForm = form.save(commit=False)
        userid = request.GET['userId']
        s = GymUser.objects.get(id=userid)
        print(s)
        addGymForm.userId = s
        addGymForm.save()
        print("Success")


    else:
        message = '你提交了空表单'
    return HttpResponse(message)
    # if request.method == 'POST':
    # 	form = addGymForm(request.POST)
    # 	if form.is_valid():
    # 		userId = request.POST.get('userId','')
    # 		entryTime = request.POST.get('entryTime', timezone.now)
    # 		add_obj = GymNow(userId = userId, entryTime = entryTime)
    # 		add_obj.save()
    # 		return HttpResponse("Success")
    # else:
    # 	form = addGymForm()
    # return HttpResponse("Unsuccess")

def SetMaxUsers(request):
	return HttpResponse("SetMaxUsers")

def AdmitUser(request):
	return HttpResponse("AdmitUser")

def LeaveGym(request):
	return HttpResponse("LeaveGym")