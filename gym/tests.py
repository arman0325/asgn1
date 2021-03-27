from django.test import Client, TestCase
from .models import GymUser, GymNow, GymWaiting, Record
from django.utils import timezone, dateformat
# Create your tests here.
from django.urls import reverse
#This is test add the user to GymUser
class GymUserModelTest(TestCase):
	def setUp(self):
		self.user1 = GymUser.objects.create(id='12133174', name='Yuen Yiu Man', userType='S')
		self.user2 = GymUser.objects.create(id='654321', name='Oliver Au', userType='E')

	def test_User(self):
		self.assertEqual(self.user1.name,'Yuen Yiu Man')
		self.assertEqual(self.user2.userType,'E')
		#none user in GymUser
		self.assertFalse(GymUser.objects.filter(id='12345678').exists())


#GymNow and GymWait is the same model data
#so there are not test two times
class GymNowModelTest(TestCase):
	def setUp(self):
		GymUser.objects.create(id='13345421', name='Peter Wong', userType='S')

	def test_addUser_to_gymRoom(self):
		user = GymUser.objects.get(pk='13345421')
		time = timezone.now()
		GymNow.objects.create(userId=user,entryTime=time)
		filterUser = GymNow.objects.filter(userId=user)[0]
		self.assertEqual(filterUser.userId, user)
		self.assertEqual(filterUser.entryTime, time)


#The record is saving the data of GymNow user leave
#the data type will be userId(fk), entryTime and waitTime
#This test is simulate a user leave the gym room and save the record
class RecordModelTest(TestCase):
	def setUp(self):
		#create GymUser
		self.user = GymUser.objects.create(id='644987', name='Terri Wong', userType='E')
		#create GymNow user
		self.enTime = timezone.now()
		#create the gym user using the gym
		GymNow.objects.create(userId=self.user,entryTime=self.enTime)

	def test_leaveGymNow(self):
		user = GymNow.objects.all()
		# save the leave time
		leavetime = dateformat.format(timezone.now(), 'Y-m-d H:i:s')
		# the model is auto add the leave time
		Record.objects.create(userId=user[0].userId, entryTime=user[0].entryTime)
		result = Record.objects.filter(userId='644987')[0]
		#check the leave time
		self.assertEqual(dateformat.format(result.leaveTime, 'Y-m-d H:i:s'),leavetime)
		self.assertEqual(result.entryTime, self.enTime)


class testView(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = GymUser.objects.create(id='644987', name='Terri Wong', userType='E')
		#create GymNow user
		self.enTime = timezone.now()
		#create the gym user using the gym
		GymNow.objects.create(userId=self.user,entryTime=self.enTime)

	def test_waitList_addtoGym(self):
		self.assertFalse(GymWaiting.objects.filter(userId='12133174').exists())
		self.user2 = GymUser.objects.create(id='12133174', name='Yuen Yiu Man', userType='S')
		self.enTime2 = timezone.now()
		self.user2Query = GymWaiting.objects.create(userId=self.user2, waitTime=self.enTime2)
		self.assertTrue(GymWaiting.objects.filter(userId='12133174').exists())

		# the user add to gym and remove from waiting list
		response = self.client.get("/gym/admit/addGym", data={"userId": "12133174"})
		self.assertFalse(GymWaiting.objects.filter(userId='12133174').exists())
		# user in gymNow
		self.assertTrue(GymNow.objects.filter(userId='12133174').exists())

	def test_waitList_removeUser(self):
		self.assertFalse(GymWaiting.objects.filter(userId='12133174').exists())
		self.user2 = GymUser.objects.create(id='12133174', name='Yuen Yiu Man', userType='S')
		self.enTime2 = timezone.now()
		self.user2Query = GymWaiting.objects.create(userId=self.user2, waitTime=self.enTime2)
		self.assertTrue(GymWaiting.objects.filter(userId='12133174').exists())

		# the user remove from waiting list
		response = self.client.get("/gym/admit/importRemove", data={"userId": "12133174"})
		self.assertFalse(GymWaiting.objects.filter(userId='12133174').exists())
		# user not in gymNow
		self.assertFalse(GymNow.objects.filter(userId='12133174').exists())

	def test_leaveGymNow(self):
		self.assertQuerysetEqual(Record.objects.all(), []) #the record none user
		# test the index response
		response = self.client.get(reverse('gym:index'))
		self.assertEqual(response.status_code, 200)
		#test the user leave the gym
		response = self.client.get("/gym/admit/leaveGym", data={"userId": "644987"})
		self.assertEqual(response.status_code, 302)
		#GymNow user query set is []
		self.assertQuerysetEqual(GymNow.objects.all(), []) 
		#GymUser nothing change
		self.assertQuerysetEqual(GymUser.objects.all(), ['<GymUser: 644987 Terri Wong>'])  
		# Record first user is 'Terri Wong'
		self.assertEqual(Record.objects.all()[0].userId.name, 'Terri Wong')

	def test_setMax(self):
		# Original max number is 8
		response = self.client.get("/gym/admit/setMax")
		self.assertEqual(response.context['maxNum'], 8)
		#modify the max number to 10
		response = self.client.get("/gym/admit/setMax", data={"maxNo": "10"})
		self.assertEqual(response.context['maxNum'], 10)

	def test_redirectView(self):
		response = self.client.get("/gym/login")
		self.assertEqual(response.status_code, 302)
		response = self.client.get("/gym/logout")
		self.assertEqual(response.status_code, 302)
