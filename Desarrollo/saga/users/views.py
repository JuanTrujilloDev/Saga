from django.shortcuts import redirect
from .forms import UserRegisterForm
from .models import User
from django.views.generic import CreateView
from django.urls import reverse

# Create your views here.

class UserCreationView(CreateView):
    model = User
    template_name = 'register.html'
    form_class = UserRegisterForm

    def get(self, request, *args: str, **kwargs):
        if request.user.is_authenticated == True:
            return(redirect(reverse('home')))
        return super().get(request, *args, **kwargs)
