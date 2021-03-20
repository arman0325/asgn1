from django.contrib import admin
from .models import GymUser, GymroomRecord

@admin.register(GymUser)
class GymUserAdmin(admin.ModelAdmin):
	list_display = ('id', 'name','userType')
	search_fields = ('id', 'name','userType')
	ordering = ('-id', 'name')

@admin.register(GymroomRecord)
class GymroomRecordAdmin(admin.ModelAdmin):
	list_display = ('time','leaveTime')