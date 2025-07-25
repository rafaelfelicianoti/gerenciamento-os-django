from django.urls import path
from .views import QuoteView, QuoteDetailView

urlpatterns = [
    path('', QuoteView.as_view(), name='quote_view'), 
    path('<int:pk>/', QuoteDetailView.as_view(), name='quote_detail'),

]
