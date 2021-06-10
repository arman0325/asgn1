from django.contrib import admin
from .models import GymUser, Record, GymNow, GymWaiting, RoomStatus

@admin.register(GymUser)
class GymUserAdmin(admin.ModelAdmin):
	list_display = ('id', 'name','userType')
	search_fields = ('id', 'name','userType')
	ordering = ('-id', 'name')

@admin.register(GymNow)
class GymNowAdmin(admin.ModelAdmin):
	list_display = ('userId', 'entryTime')
	ordering = ('entryTime',)

@admin.register(GymWaiting)
class GymWaitingAdmin(admin.ModelAdmin):
	list_display = ('userId', 'waitTime')
	ordering = ('waitTime',)

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
	list_display = ('userId', 'entryTime','leaveTime')
	ordering = ('entryTime',)

@admin.register(RoomStatus)
class RecordAdmin(admin.ModelAdmin):
	list_display = ('roomId', 'roomName','roomAction','roomStatus')
	ordering = ('roomId',)