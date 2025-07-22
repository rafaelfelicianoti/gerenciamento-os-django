from django.urls import path
from . import views

urlpatterns = [
    path('', views.Employee_view, name='employee_view'), 
]
