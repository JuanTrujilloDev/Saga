from django.db.models.signals import m2m_changed, pre_save
from .models import Projecto, Tarea
from django.dispatch import receiver


@receiver(m2m_changed, sender = Projecto.miembros.through)
def project_users_change(sender, instance, action, **kwargs):
    if action == 'pre_remove':
        miembros = instance.miembros.all()
        for miembro in miembros:
            tareas = Tarea.objects.filter(miembros = miembro)
            for tarea in tareas:
                tarea.miembros.remove(miembro)

@receiver(pre_save, sender = Projecto)
def project_encargado_change(sender, instance, **kwargs):
    previous = Projecto.objects.get(id = instance.id).encargado
    if instance.encargado != previous:
        tareas = Tarea.objects.filter(miembros = previous)
        for tarea in tareas:
            tarea.miembros.remove(previous)
