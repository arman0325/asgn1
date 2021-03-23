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
		return f'{self.id} {self.name}'
		

class GymNow(models.Model):
	userId = models.ForeignKey(GymUser,
                              on_delete=models.CASCADE,
                              related_name='GymNow')
	entryTime = models.DateTimeField(default=timezone.now)
	objects = models.Manager()

	class Meta:
		ordering = ('-entryTime',)

	def __str__(self):
		return f'{self.userId} entry at {self.entryTime}'

class GymWaiting(models.Model):
	userId = models.ForeignKey(GymUser,
                              on_delete=models.CASCADE,
                              related_name='GymWaiting')
	waitTime = models.DateTimeField(default=timezone.now)
	objects = models.Manager()

	class Meta:
		ordering = ('-waitTime',)

	def __str__(self):
		return f'{self.userId} wait from {self.waitTime}'


class Record(models.Model):
	userId = models.ForeignKey(GymUser,
                              on_delete=models.CASCADE,
                              related_name='GymRoom')
	entryTime = models.DateTimeField(default=None)
	leaveTime= models.DateTimeField(auto_now=True)
	objects = models.Manager()

	class Meta:
		ordering = ('-entryTime',)

	def __str__(self):
		return f'{self.userId} entry at {self.entryTime} and leave at {self.leaveTime}'