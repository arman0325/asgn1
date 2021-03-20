import csv
from django.shortcuts import render
from django.http import HttpResponse

from .models import GymUser
# Create your views here.
def exportGymUser(request):
	response = HttpResponse(content_type='text/csv')

	writer = csv.writer(response)
	writer.writerow(['ID','Name','User Type'])

	for user in GymUser.objects.all().values_list('id','name','userType'):
		writer.writerow(user)

	response['Content-Disposition'] = 'attachment; filename="GymUser.csv"'
	return response

def index(request):
	users = GymUser.objects.all()
	return render(request, 'gym/index.html',{'users':users})