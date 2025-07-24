from rest_framework import serializers
from .models import Quote
from client.models import Client

class QuoteSerializer(serializers.ModelSerializer):
    
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(),
        source='client'  # Mapeia o client_id do JSON para o campo client do model
    )
    class Meta:
        model = Quote
        fields = [
            'id', 
            'client_id',
            'description', 
            'status', 
            'labor_cost', 
            'materials_cost', 
            'total_value', 
            'created_at'
        ]