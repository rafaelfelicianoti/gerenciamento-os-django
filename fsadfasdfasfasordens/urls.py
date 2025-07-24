from django.urls import path, include

urlpatterns = [
    path('client/', include('ordens.client.urls')),
    path('employee/', include('ordens.employee.urls')),
]
