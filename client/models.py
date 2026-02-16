# MELHORIAS:
    # incluir endereço
    # validar cpf cnpj

from django.db import models

# clientes
class Client(models.Model):
    name = models.CharField(max_length=255 )
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
    cpf_cnpj = models.CharField(
        max_length = 18, 
        unique = True,
        blank = False,
        null = False
    )

    def __str__(self):
        return f"{self.name} - {self.email} - {self.phone} - {self.cpf_cnpj}"
    
