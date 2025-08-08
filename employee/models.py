from django.db import models
from users.models import User

# Funcionarios 
class Employee(models.Model):
    ROLE_CHOICES = [
        ('gerente' , 'Gerente'),
        ('secretaria', 'Secretaria'),
        ('operador', 'Operador'),
        ('encarregado', 'Encarregado'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length = 11)

    def __str__(self):
        return f'{self.name} ({self.role})'