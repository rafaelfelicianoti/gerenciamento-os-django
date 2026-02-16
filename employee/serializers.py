from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from .models import Employee

User = get_user_model()

# Cria o employee e o user associado
class EmployeeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(
        write_only=True,
        min_length=4,
        error_messages={
            "min_length": "A senha precisa ter pelo menos 4 caracteres."
        }
    )

    class Meta:
        model = Employee
        fields = ['id', 'name', 'role', 'phone', 'email', 'password']

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        try:
            user = User.objects.create_user(email=email, password=password)
        except IntegrityError:
            raise ValidationError({'email': 'Este e-mail já está em uso.'})

        employee = Employee.objects.create(user=user, **validated_data)
        return employee

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['email'] = instance.user.email if instance.user else None
        return rep
