from typing import List
from django.shortcuts import redirect, render, get_object_or_404, HttpResponseRedirect
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView
from .models import Projecto, Tarea
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from users.models import User
from .forms import TareaCreate

# Create your views here.
class MainTrabajador(LoginRequiredMixin, ListView):
    template_name="main-trabajador.html"
    model = Projecto

    def get_queryset(self):
        queryset = Projecto.objects.filter(Q(fecha_final__gte = timezone.now())).order_by('fecha_final')
        queryset = queryset.exclude(Q(estado = 3) & Q(estado = 4))
        queryset = queryset.filter((Q(miembros__id = self.request.user.pk ) | Q(encargado__id = self.request.user.pk))).distinct()
        return queryset

    def get(self, request, *args, **kwargs):
        if request.user.get_grupo() == 'Trabajador':
            return super().get(request, *args, **kwargs)
        else:
            return(redirect(reverse('main-admin')))

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        tareas = Tarea.objects.filter(Q(miembros__id = self.request.user.pk) & Q(fecha_finest__gte = timezone.now())).order_by('-fecha_finest').distinct()
        context['tareas'] = tareas.exclude(estado = 6)[0:4]
        return context


class MainAdmin(LoginRequiredMixin, ListView):
    template_name = "main-admin.html"
    model = Projecto

    def get_queryset(self):
        queryset = Projecto.objects.filter(Q(fecha_final__gte = timezone.now())).order_by('fecha_final')
        queryset = queryset.exclude(Q(estado = 3) & Q(estado = 4))
        queryset = queryset.filter((Q(miembros__id = self.request.user.pk ) | Q(encargado__id = self.request.user.pk))).distinct()
        return queryset

    def get(self,request, *args, **kwargs):
        if request.user.get_grupo() == 'Administrador':
            return super().get(request, *args, **kwargs)
        else:
            return(redirect(reverse('main-trabajador')))
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        tareas = Tarea.objects.filter(Q(miembros__id = self.request.user.pk) & Q(fecha_finest__gte = timezone.now())).order_by('-fecha_finest').distinct()
        context['tareas'] = tareas.exclude(estado = 6)[0:4]

        trabajadores = User.objects.filter(groups__name = 'Trabajador').order_by('last_name')
        context['trabajadores'] = trabajadores
        return context










class TareaUpdate(LoginRequiredMixin, UpdateView):
    model = Tarea
    template_name = "tarea-update.html"
    fields = ['nombre', 'estado', 'descripcion', 'miembros']

    def get(self, request, *args: str, **kwargs):
        if self.request.user in self.get_object().miembros.all() or self.request.user.groups.name == "Administrador":
            return super().get(request, *args, **kwargs)
        else:
            return(redirect('projecto-detail', kwargs = {"pk": self.get_object().pk}))




class TareaCreateView(LoginRequiredMixin,  DetailView):
    model = Projecto
    template_name = "tarea-create.html"
    

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'form': TareaCreate()
        })
        return ctx

    def post(self, *args, **kwargs):
        self.object = self.get_object(self.get_queryset())
        form = TareaCreate(self.request.POST)
        if form.is_valid():
            form.instance.projecto = self.object
            form.save()
            return HttpResponseRedirect(self.object.get_absolute_url())
        else:
            ctx = self.get_context_data(**kwargs)
            ctx.update({'form': form})
            return self.render_to_response(ctx)

    def get(self, request, *args, **kwargs):
        if self.request.user in self.get_object().miembros.all() or self.request.user == self.get_object().encargado:
            return super().get(request, *args, **kwargs)
        else:
            return(redirect('main-admin'))



class ProjectDetail(LoginRequiredMixin, DetailView):
    template_name = "project-detail.html"
    model = Projecto

    def get(self, request, *args, **kwargs):
        if self.request.user == self.get_object().encargado or self.request.user in self.get_object().miembros.all():
            return super().get(request, *args, **kwargs)
        if self.request.user.groups.name == "Administrador":
            return(redirect(reverse('main-admin')))
        else:
            return(redirect(reverse('main-admin')))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['backlog'] = Tarea.objects.filter(estado = 0)
        context['diseño'] = Tarea.objects.filter(estado = 1)
        context['desarrollo'] = Tarea.objects.filter(estado = 2)
        context['testing'] = Tarea.objects.filter(estado = 3)
        context['review'] = Tarea.objects.filter(estado = 4)
        context['done'] = Tarea.objects.filter(estado = 5)
        return context

class ProjectoUpdate(LoginRequiredMixin, UpdateView):
    model = Projecto
    template_name = "projecto-update.html"
    fields = ['nombre_clave', 'nombre_comercial', 'fecha_final', 'descripcion', 'estado', 'miembros', 'encargado']

    def get(self, request, *args: str, **kwargs):
        if self.request.user == self.get_object().encargado or self.request.user.groups.name == "Administrador":
            return super().get(request, *args, **kwargs)
        else:
            return(redirect(self.get_object().get_absolute_url()))




class ProjectoCreate(LoginRequiredMixin, CreateView):
    model = Projecto
    template_name = "projecto-create.html"
    fields = ['nombre_clave', 'nombre_comercial', 'fecha_final', 'descripcion', 'estado', 'miembros', 'encargado']

    def get(self, request, *args: str, **kwargs):
        if  self.request.user.groups.name == "Administrador":
            return super().get(request, *args, **kwargs)
        else:
            return(redirect('main-admin'))

class ProjectoDelete(LoginRequiredMixin, DeleteView):
    model = Projecto
    template_name = 'projecto-delete.html'

    def get(self, request, *args: str, **kwargs):
        if self.request.user == self.get_object().encargado or self.request.user.groups.name == "Administrador":
            return super().get(request, *args, **kwargs)
        else:
            return(redirect('projecto-delete', kwargs = {"pk": self.get_object().pk}))

class TareaDelete(LoginRequiredMixin, DeleteView):
    model = Tarea
    template_name = "tarea-delete.html"

    def get(self, request, *args: str, **kwargs):
        if self.request.user in self.get_object().miembros.all() or self.request.user.groups.name == "Administrador":
            return super().get(request, *args, **kwargs)
        else:
            return(redirect('projecto-delete', kwargs = {"pk": self.get_object().pk}))


