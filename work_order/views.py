from rest_framework.response import Response
from rest_framework import status
from .serializers import WorkOrderSerializer
from rest_framework.views import APIView
from .models import WorkOrder
from django.http import Http404


class WorkOrderView(APIView):

    def post(self, request):
        serializer = WorkOrderSerializer(data=request.data)
        if serializer.is_valid():
            work_order = serializer.save()
            return Response(WorkOrderSerializer(work_order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, format=None):
        work_order = WorkOrder.objects.all()
        serializer = WorkOrderSerializer(work_order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class WorkOrderDetailView(APIView):
     
    # busca o quote pelo id
    def get_object(self, pk):
        try:
            return WorkOrder.objects.get(pk=pk)
        except WorkOrder.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        work_order = self.get_object(pk)
        serializer = WorkOrderSerializer(work_order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        work_order = self.get_object(pk)
        serializer = WorkOrderSerializer(work_order, data=request.data)
        if serializer.is_valid():
            work_order = serializer.save()
            return Response(WorkOrderSerializer(work_order).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete (self, request, pk, format=None):
        work_order = self.get_object(pk)
        work_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)