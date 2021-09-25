from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.

class User(AbstractUser):
    documento_regex = RegexValidator(regex='^[0-9]{6,10}$')
    username = models.CharField(validators=[documento_regex], max_length=10, unique=True, null=False, blank=False, verbose_name="Numero de documento")
    phone_regex = RegexValidator(regex='^(3)([0-9]){9}$', message = "Por favor escribe el numero en el formato aceptado sin código de área ej: 3123456789")
    telefono = models.CharField(validators=[phone_regex], max_length=10, verbose_name="Telefono", unique=True)
    direccion = models.CharField(max_length= 70, verbose_name="Direccion")
    incorporado = models.DateField(auto_now_add=True, null=True, blank=True)


