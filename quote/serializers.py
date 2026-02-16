from rest_framework import serializers
from .models import Quote
from client.serializers import ClientSerializer

class QuoteSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    class Meta:
        model = Quote
        fields = [
            'id', 
            'client',
            'description', 
            'status', 
            'labor_cost', 
            'materials_cost', 
            'total_value', 
            'created_at'
        ]