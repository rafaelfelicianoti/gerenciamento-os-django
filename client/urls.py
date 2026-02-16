from django.urls import path
from .views import ClientView, ClientDetailView

urlpatterns = [
    path('', ClientView.as_view(), name='client_view'),
    path('<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
]