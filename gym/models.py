from django.db import models
from django.utils import timezone

class GymUser(models.Model):
	USER_TYPES = (
		('S', 'Student'),
		('E', 'Employee')
	)

	id = models.CharField(max_length = 8, primary_key = True)
	name = models.CharField(max_length = 32)
	userType = models.CharField(max_length = 1, choices = USER_TYPES, default = 'S')

	objects = models.Manager()

	class Meta:
		ordering = ('-id',)

	def __str__(self):
		return self.name
		

class GymroomRecord(models.Model):
	"""docstring for GymRoom"""
	userId = models.ForeignKey(GymUser,
                              on_delete=models.CASCADE,
                              related_name='GymRoom')
	time = models.DateTimeField(default=None)
	leaveTime= models.DateTimeField(default=timezone.now)
	objects = models.Manager()

	class Meta:
		ordering = ('-time',)

	def __str__(self):
		return self.userId