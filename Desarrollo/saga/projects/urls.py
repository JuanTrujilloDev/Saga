"""saga URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import MainAdmin, MainTrabajador, ProjectDetail, TareaUpdate, TareaCreateView, ProjectoCreate, ProjectoUpdate, ProjectoDelete, TareaDelete

urlpatterns = [
    path('main-trabajador/', MainTrabajador.as_view(), name="main-trabajador"),
    path('main-admin/', MainAdmin.as_view(), name="main-admin"),
    path('projecto-table/<str:pk>/<str:slug>', ProjectDetail.as_view(), name="project-detail"),
    path('tarea-update/<str:pk>', TareaUpdate.as_view(), name="tarea-update"),
    path('tarea-delete/<str:pk>', TareaDelete.as_view(), name="tarea-delete"),
    path('tarea-create/<str:pk>/<str:slug>', TareaCreateView.as_view(), name="tarea-create"),
    path('projecto-create', ProjectoCreate.as_view(), name="projecto-create"),
    path('projecto-update/<str:pk>/<str:slug>', ProjectoUpdate.as_view(), name="projecto-update"),
    path('projecto-delete/<str:pk>/<str:slug>', ProjectoDelete.as_view(), name="projecto-delete"),
    

]
