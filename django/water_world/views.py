from django.shortcuts import render
from django.views import generic

from .models import Event, WaterPump


class EventView(generic.base.TemplateView):
    template_name = "water_world/events.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_events'] = Event.objects.all().order_by('-event_time')[:40]
        
        return context


class PumpView(generic.base.TemplateView):
    template_name = "water_world/pump.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_actions'] = WaterPump.objects.all().order_by('-pump_activated')[:40]
        
        return context
