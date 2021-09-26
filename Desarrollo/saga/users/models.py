from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.core.validators import RegexValidator
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

class User(AbstractUser):
    documento_regex = RegexValidator(regex='^[0-9]{6,10}$')
    username = models.CharField(validators=[documento_regex], max_length=10, unique=True, null=False, blank=False, verbose_name="Numero de documento")
    phone_regex = RegexValidator(regex='^(3)([0-9]){9}$', message = "Por favor escribe el numero en el formato aceptado sin código de área ej: 3123456789")
    telefono = models.CharField(validators=[phone_regex], max_length=10, verbose_name="Telefono", unique=True)
    direccion = models.CharField(max_length= 70, verbose_name="Direccion")
    incorporado = models.DateField(auto_now_add=True, null=True, blank=True)
    groups = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL, default=0)
    email = models.EmailField(blank = False, unique=True, verbose_name="Email")
    slug = models.SlugField(null = True, blank=True)

    class Meta:
        ordering = ['last_name']

    def get_grupo(self):
        return self.groups.name

    def __str__(self):
        nombre = self.first_name +" " + self.last_name
        return nombre

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("user-update", kwargs={"slug": self.slug})
    



