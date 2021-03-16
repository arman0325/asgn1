from django.db import models
from django.utils import timezone
class Student(models.Model):
    StuId =  models.CharField(max_length=8)
    name = models.CharField(max_length=32)

    objects = models.Manager()
    class Meta:
        ordering = ('-StuId',)
    def __str__(self):
        return self.name

class Employee(models.Model):
    EmpId =  models.CharField(max_length=8)
    name = models.CharField(max_length=32)
    
    objects = models.Manager()
    class Meta:
        ordering = ('-EmpId',)
    def __str__(self):
        return self.name