from .serializers import QuoteSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch') 
class QuoteView(APIView):
    def post(self, request):
        serializer = QuoteSerializer(data=request.data)
        if serializer.is_valid():
            quote = serializer.save()
            return Response(QuoteSerializer(quote).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)