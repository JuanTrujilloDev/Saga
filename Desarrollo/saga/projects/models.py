from djongo import models
from users.models import User
import uuid
from django.db.models import Q
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

class Projecto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_clave = models.CharField(max_length=30, verbose_name="Nombre Clave", unique=True)
    nombre_comercial = models.CharField(max_length=30, verbose_name="Nombre Comercial")
    fecha_inicio = models.DateTimeField(auto_now_add = True)
    fecha_final = models.DateTimeField(auto_now = False, auto_now_add=False)
    descripcion = models.TextField(max_length= 80, null =True, blank = True)
    estados = [
        (1, ("Confirmado")),
        (2, ("Desarrollo")),
        (3, ("Finalizado")),
        (4, ("Cancelado"))
    ]

    estado = models.IntegerField(choices = estados, default = estados[0])
    encargado = models.ForeignKey(to = User, on_delete= models.CASCADE, null = True, related_name="encargado")
    miembros = models.ManyToManyField(to = User, blank=True, related_name="miembros")
    slug = models.SlugField(null = True, blank=True, unique=True)

    class Meta:
        ordering = ['-fecha_final']

    def get_numtareas(self):
        tareas = Tarea.objects.filter(projecto = self).count()
        return tareas

    def get_tareascomp(self):
        tareas = Tarea.objects.filter(Q(projecto = self ) & Q(estado = 6)).count()
        return tareas

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre_clave)
        super().save( *args, **kwargs)

    def get_absolute_url(self):
        return reverse("project-detail", kwargs={"pk": self.pk, "slug":self.slug})

    def get_tarea_create_url(self):
        return reverse("tarea-create", kwargs={"pk": self.pk, "slug":self.slug})

    def get_edit_url(self):
        return reverse("projecto-update", kwargs={"pk": self.pk, "slug":self.slug})

    def get_delete_url(self):
        return reverse("projecto-delete", kwargs={"pk": self.pk, "slug":self.slug})
    



class Tarea(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    estados = [
        (1, ("Backlog")),
        (2, ("Diseño")),
        (3, ("Desarrollo")),
        (4, ("Testing")),
        (5, ("Review")),
        (6, ("Done"))
    ]
    nombre = models.CharField(max_length= 25, verbose_name="Nombre")
    estado = models.IntegerField(choices = estados, default= estados[0])
    fecha_inest = models.DateTimeField(auto_now= False, auto_now_add= False)
    fecha_finest = models.DateTimeField(auto_now=False, auto_now_add=False)
    duracion_est = models.DurationField(null=True)
    duracion_real = models.DurationField(null=True, blank=True)
    descripcion = models.TextField(max_length=120, null= True, blank = True)

    miembros = models.ArrayReferenceField(
        to = User,
        on_delete= models.SET_NULL,
        null = True,
        blank = True
    )


    projecto = models.ForeignKey(
        to= Projecto,
        on_delete= models.CASCADE,
        null = True
    )

    def get_absolute_url(self):
        return reverse("tarea-update", kwargs={"pk": self.pk})

    
    

class Archivo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length= 25, verbose_name="Nombre")
    file = models.FileField(upload_to='archivos')
    descripcion = models.TextField(max_length= 80, verbose_name= "Archivo")
    tipo_archivo = [
        (1, ("Codigo")),
        (2, ("Modelos")),
        (3, ("Mockups")),
        (4, ("Documentos")),
        (5, ("Otros"))
    ]
    tipo = models.IntegerField(choices= tipo_archivo, null = True)
    autor = models.ForeignKey(
        to = User,
        on_delete= models.SET_NULL,
        null = True
    )
    tarea = models.ForeignKey(
        to = Tarea,
        on_delete= models.CASCADE,
        null = False
    )


