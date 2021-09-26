from django.shortcuts import redirect
from .forms import UserRegisterForm
from .models import User
from django.views.generic import CreateView, UpdateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class UserCreationView(CreateView):
    model = User
    template_name = 'register.html'
    form_class = UserRegisterForm

    def get(self, request, *args: str, **kwargs):
        if request.user.is_authenticated == True:
            return(redirect(reverse('home')))
        return super().get(request, *args, **kwargs) 

class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "edit-profile.html"
    model = User
    fields = ['username', 'email', 'first_name', 'last_name', 'telefono', 'direccion']

    def get(self, request, *args, **kwargs):
        if self.request.user.groups.name == 'Administrador' or self.request.user == self.get_object():
            if self.get_object().groups.name == 'Administrador' and self.request.user != self.get_object():
                return(redirect(reverse('user-update' , kwargs = {'slug': self.request.user.slug})))

            return super().get(request, *args, **kwargs)
        return(redirect(reverse('user-update', kwargs = {'slug': self.request.user.slug})))

    def get_success_url(self) -> str:
        return(reverse('user-update', kwargs = {'slug': self.request.user.slug}))
