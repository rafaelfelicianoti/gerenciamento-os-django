from django.urls import path
from .views import ClientView, ClienDetailView

urlpatterns = [
    path('', ClientView.as_view(), name='client_view'),
    path('<int:pk>/', ClienDetailView.as_view(), name='client_detail'),
]