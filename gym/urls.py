from django.urls import path
from . import views

app_name = 'gym'

urlpatterns = [
    # post views
    #Path: /gym/
    path('', views.index, name='index'),
    #Path: /gym/gymroom
    path('gymroom', views.viewCurrentUsers, name='viewCurrentUsers'),
    #Path: /gym/login
    path('login', views.easyLogin, name='easyLogin'),
    #Path: /gym/logout
    path('logout', views.easyLogout, name='easyLogout'),
    #Path: /gym/admit/lsit
    path('admit/list', views.list, name='list'),
    #Path: /gym/admit/admitGym
    path('admit/admitGym', views.viewCurrentUsers, name='admitGym'),
    #Path: /gym/admit/upload
    path('admit/upload', views.upload, name='upload'),
    #Path: /gym/admit/export
    path('admit/export', views.exportGymUser, name='export_GymUser'),
    #Path: /gym/admit/addForm
    path('admit/addForm', views.addForm, name='addForm'),
    #Path: /gym/admit/leaveGym
    path('admit/leaveGym', views.LeaveGym, name='LeaveGym'),
    #Path: /gym/admit/addGym
    path('admit/addGym', views.addGym, name='addGym'),
    #Path: /gym/admit/importRemove
    path('admit/importRemove', views.importRemove, name='importRemove'),
    #Path: /gym/admit/setMax
    path('admit/setMax', views.SetMaxUsers, name='SetMaxUsers'),

]
