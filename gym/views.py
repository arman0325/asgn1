import csv
from django.shortcuts import render
from django.http import HttpResponse

from .models import Student
# Create your views here.
def export(request):
	response = HttpResponse(content_type='text/csv')

	writer = csv.writer(response)
	writer.writerow(['Student ID','Name'])

	for student in Student.objects.all().values_list('StuId','name'):
		writer.writerow(student)

	response['Content-Disposition'] = 'attachment; filename="student.csv"'
	return response