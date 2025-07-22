from django.db import models

# Funcionarios 
class Employee(models.Model):
    ROLE_CHOICES = [
        ('gerente' , 'Gerente'),
        ('secretaria', 'Secretaria'),
        ('operador', 'Operador'),
        ('encarregado', 'Encarregado'),
    ]
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    email = models.EmailField(
        max_length = 255, 
        unique = True,
        blank = False,
        null = False
    )
    phone = models.CharField(
        max_length = 11, 
        blank = False,
        null = False
    )