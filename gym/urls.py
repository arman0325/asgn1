from django.urls import path
from . import views

app_name = 'gym'

urlpatterns = [
    # post views
    path('', views.export, name='export'),
    

]
