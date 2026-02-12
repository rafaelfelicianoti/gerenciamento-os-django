from django.db import models
from quote.models import Quote
from django.core.exceptions import ValidationError


class WorkOrder(models.Model):
    STATUS_CHOICES=[
        ('aberto', 'Aberto'),
        ('em_andamento', 'Em Andamento'),
        ('concluido', 'Concluido'),
        ('cancelado', 'Cancelado')
    ]
    quote = models.ForeignKey(
        Quote, 
        on_delete=models.CASCADE,
        related_name='work_orders'
    )

    description = models.TextField(
        blank=False,
        null = False
    )

    opened_at = models.DateTimeField(auto_now_add=True)

    completed_at = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
            default='aberto'
    )

    "Só é possível criar uma OS com orçamento aprovado."
    def clean(self):
        if self.quote.status != 'aprovado':
             raise ValidationError('O orçamento precisa estar aprovado.')

    def save(self, *args, **kwargs):
        self.full_clean()   
        super().save(*args, **kwargs)

    @property
    def total_value(self):
        if self.quote.status == 'aprovado':
            return self.quote.total_value

