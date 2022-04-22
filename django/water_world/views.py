from django.shortcuts import render
from django.views import generic

from .models import Config


class ConfigView(generic.base.View):
    template_name = "water_world/config.html"
    context_object_name = "config"

    def get_queryset(self):
        """
        Return the last config.
        """
        return Config.objects.all()[0]
