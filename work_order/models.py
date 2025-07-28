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

    completed_at = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )

    @property
    def total_value(self):
        if self.quote.status == 'aprovado':
            return self.quote.total_value

    # sava apenas se o orcamento estiver aprovado
    def save(self, *args, **kwargs): 
        if self.quote.status != 'aprovado':
            raise ValidationError("Orçamento nao esta aprovado")
        super().save(*args, **kwargs)