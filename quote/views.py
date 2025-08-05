from .models import Quote
from .serializers import QuoteSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import Http404


@method_decorator(csrf_exempt, name='dispatch') 
class QuoteView(APIView):

    def post(self, request):
        serializer = QuoteSerializer(data=request.data)
        if serializer.is_valid():
            quote = serializer.save()
            return Response(QuoteSerializer(quote).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        quote = Quote.objects.all()
        serializer = QuoteSerializer(quote, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@method_decorator(csrf_exempt, name='dispatch') 
class QuoteDetailView(APIView):
     
    # busca o quote pelo id
    def get_object(self, pk):
        try:
            return Quote.objects.get(pk=pk)
        except Quote.DoesNotExist:
            raise Http404

    # faz o get de acodo como id
    def get(self, request, pk, format=None):
        quote = self.get_object(pk)
        serializer = QuoteSerializer(quote)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk, format=None):
        quote = self.get_object(pk)
        serializer = QuoteSerializer(quote, data=request.data)
        if serializer.is_valid():
            quote = serializer.save()
            return Response(QuoteSerializer(quote).data, status=status.HTTP_200_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        quote = self.get_object(pk)
        quote.delete()
        return Response(status.HTTP_204_NO_CONTENT)