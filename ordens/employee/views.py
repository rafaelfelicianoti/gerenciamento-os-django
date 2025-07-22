from .serializers import EmployeeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view



@api_view(['POST'])
def Employee_view(request):
    if request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        is_valid = serializer.is_valid()
        
        print(f'REQUEST ', request.data)
        print(f'IS VALID ', is_valid)
        print(f'ERRORS', serializer.errors)
        print(f'VALIDATEDDATA', serializer.validated_data)
        if serializer.is_valid():
            employee = serializer.save()
            return Response(EmployeeSerializer(employee).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
    