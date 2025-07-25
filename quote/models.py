from django.db import models
from client.models import Client

# Oçamento
class Quote(models.Model):
    STATUS_CHOICES=[
        ('aberto','Aberto'),
        ('enviado', 'Enviado'),
        ('aprovado', 'Aprovado'),
        ('recusado', 'Recusado'),
        ('cancelado', 'Cancelado'),
    ]

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE, 
        related_name='quotes'
    )
    
    description = models.TextField(
        blank=False,
        null=False,
    )
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES
    )
    
    labor_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00
    )
    
    materials_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00
    )
    
    total_value = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        editable=False
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    # calcula o total de material e servico
    def save(self, *args, **kwargs):
        self.total_value = self.labor_cost + self.materials_cost
        super().save(*args, **kwargs)


