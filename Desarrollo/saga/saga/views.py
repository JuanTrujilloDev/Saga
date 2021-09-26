from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class HomeView (TemplateView):
    template_name="home.html"




