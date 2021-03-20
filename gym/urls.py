from django.urls import path
from . import views

app_name = 'gym'

urlpatterns = [
    # post views
    path('export', views.exportGymUser, name='export_GymUser'),
    path('', views.index, name='index'),

]
