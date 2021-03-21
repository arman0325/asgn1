from django.urls import path
from . import views

app_name = 'gym'

urlpatterns = [
    # post views
    path('export', views.exportGymUser, name='export_GymUser'),
    path('', views.index, name='index'),
    path('gymroom', views.viewCurrentUsers, name='viewCurrentUsers'),
    path('addGym', views.addGym, name='addGym'),
    path('addForm', views.addForm, name='addForm'),

]
