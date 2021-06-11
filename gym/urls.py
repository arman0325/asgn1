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
    path('login', views.userLogin, name='userLogin'),
    #Path: /gym/logout
    path('logout', views.Logout, name='Logout'),
    #Path: /gym/admit/lsit
    path('admit/list', views.list, name='list'),
    #Path: /gym/admit/admitGym
    path('admit/admitGym', views.viewCurrentUsers, name='admitGym'),
    #Path: /gym/admit/upload
    path('admit/upload', views.upload, name='upload'),
    #Path: /gym/admit/export
    path('admit/export', views.exportGymUser, name='export_GymUser'),
    #Path: /gym/admit/leaveGym
    path('admit/leaveGym', views.LeaveGym, name='LeaveGym'),
    #Path: /gym/admit/addGym
    path('admit/addGym', views.addGym, name='addGym'),
    #Path: /gym/admit/importRemove
    path('admit/importRemove', views.importRemove, name='importRemove'),
    #Path: /gym/admit/setMax
    path('admit/setMax', views.SetMaxUsers, name='SetMaxUsers'),
    #Path: /gym/admit/record
    path('admit/record', views.viewRecord, name='viewRecord'),
    #Path: /gym/admit/record/12133174
    path('admit/record/<int:id>/', views.viewRecord, name='viewRecord'),
    #Path: /gym/admit/cleanGym
    path('admit/cleanGym', views.cleanGym, name='cleanGym'),
    #Path: /gym/admit/GymStatus
    path('admit/GymStatus', views.GymStatus, name='GymStatus'),
    #Path: /gym/admit/addUser/0
    path('admit/addUser/<int:type>', views.addPage, name='addPage'),

]

handler404="gym.views.handle_not_found" # for 404 page but the debug need to change to False