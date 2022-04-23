from django.contrib import admin

from django.contrib import admin
from .models import Config, Event, WaterPump


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("event_time", "event_type", "message")


@admin.register(WaterPump)
class WaterPumpAdmin(admin.ModelAdmin):
    list_display = ("pump_activated", "pump_stopped")

admin.site.register([Config])
