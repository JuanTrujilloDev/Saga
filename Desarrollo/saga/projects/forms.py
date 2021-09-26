from django.db.models.base import Model
from django.forms import ModelForm
from .models import Tarea


class TareaCreate(ModelForm):
    
    class Meta:
        model = Tarea
        fields = ['nombre', 'fecha_inest', 'fecha_finest', 'duracion_est', 'descripcion', 'miembros']

