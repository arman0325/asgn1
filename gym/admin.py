from django.contrib import admin
from .models import Student
from .models import Employee

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('StuId', 'name')
    search_fields = ('StuId', 'name')
    ordering = ('StuId', 'name')

@admin.register(Employee)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('EmpId', 'name')
    search_fields = ('EmpId', 'name')
    ordering = ('EmpId', 'name')
