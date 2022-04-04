from django.shortcuts import render
from django.views import generic

from .models import Config


class IndexView(generic.ListView):
    template_name = "water_world/index.html"
    context_object_name = "config"

    def get_queryset(self):
        """
        Return the last config.
        """
        return Config.objects.all()[0]
