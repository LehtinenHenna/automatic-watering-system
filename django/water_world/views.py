from django.shortcuts import render
from django.views import generic

from .models import Config, Event, WaterPump


class ConfigView(generic.base.View):
    template_name = "water_world/config.html"
    context_object_name = "config"

    def get_queryset(self):
        """
        Return the last config.
        """
        return Config.objects.all()[0]


class EventView(generic.base.TemplateView):
    template_name = "water_world/events.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_events'] = Event.objects.all()[:30]
        
        return context


class PumpView(generic.base.TemplateView):
    template_name = "water_world/pump.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_actions'] = WaterPump.objects.all()[:30]
        
        return context
