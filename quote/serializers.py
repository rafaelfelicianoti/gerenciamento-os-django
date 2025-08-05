from rest_framework import serializers
from .models import Quote
from client.models import Client

# pega tosdos os dados do client para mostrar junto ao orcamento
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'id',
            'name', 
            'email', 
            'phone', 
            'cpf_cnpj'
        ]

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