from rest_framework import serializers
from .models import WorkOrder

class WorkOrderSerializer(serializers.ModelSerializer):
    total_value = serializers.DecimalField(
        max_digits=10,        
        decimal_places=2,     
        read_only=True        
    )

    class Meta:
        model = WorkOrder
        fields = [
            'id',
            'quote',
            'description',
            'opened_at',
            'completed_at',
            'status',
            'total_value'
        ]


    # sava apenas se o orcamento estiver aprovado
    def validate_quote(self, quote):
        if quote.status != 'aprovado':
            raise serializers.ValidationError("O orçamento precisa estar aprovado.")
        return quote