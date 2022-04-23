from django.contrib import admin

from django.contrib import admin
from .models import Config, Event, WaterPump


#@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Event message", {"fields": ["message"]}),
        ("Event type", {"fields": ["event_type"]}),
        ("Event time", {"fields": ["event_time"]}),
    ]
    list_display = ("message", "event_type", "event_time")


@admin.register(WaterPump)
class WaterPumpAdmin(admin.ModelAdmin):
    list_display = ("pump_activated", "pump_stopped")

admin.site.register([Config, Event])
