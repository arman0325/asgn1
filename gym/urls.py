from django.urls import path
from . import views

app_name = 'gym'

urlpatterns = [
    # post views
    #Path: /gym/
    path('', views.index, name='index'),
    #Path: /gym/export
    path('export', views.exportGymUser, name='export_GymUser'),
    #Path: /gym/gymroom
    path('gymroom', views.viewCurrentUsers, name='viewCurrentUsers'),
    #Path: /gym/importRemove
    path('importRemove', views.importRemove, name='importRemove'),
    #Path: /gym/importnew
    path('importnew', views.importNew, name='importNew'),
    #Path: /gym/admit/admitGym
    path('admit/admitGym', views.AdmitUser, name='admitGym'),
    #Path: /gym/admit/addGym
    path('admit/addGym', views.addGym, name='addGym'),
    #Path: /gym/admit/leaveGym
    path('admit/leaveGym', views.LeaveGym, name='LeaveGym'),
    #Path: /gym/admit/addForm
    path('admit/addForm', views.addForm, name='addForm'),
    #Path: /gym/admit/addUser
    path('admit/addUser', views.importNew, name='importNew'),
    #Path: /gym/setMax
    path('admit/setMax', views.SetMaxUsers, name='SetMaxUsers'),



]
