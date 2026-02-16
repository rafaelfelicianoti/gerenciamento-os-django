from django.urls import path
from .views import WorkOrderView, WorkOrderDetailView

urlpatterns = [
    path('', WorkOrderView.as_view(), name='work_order'),
    path('<int:pk>/', WorkOrderDetailView.as_view(), name='work_order_detail'),
]