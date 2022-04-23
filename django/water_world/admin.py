from django.contrib import admin

from django.contrib import admin
from .models import Config, Event, WaterPump

#@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Enable system", {"fields": ["enable_system"]}),
        ("Seconds to pump", {"fields": ["liters_to_pump"]}),
        ("Sensor read interval (hours)", {"fields": ["sensor_read_interval_hours"]}),
    ]
    list_display = ("enable_system", "liters_to_pump", "sensor_read_interval_hours")

#@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Event message", {"fields": ["message"]}),
        ("Event type", {"fields": ["event_type"]}),
        ("Event time", {"fields": ["event_time"]}),
    ]
    list_display = ("message", "event_type", "event_time")


admin.site.register([Config, Event, WaterPump])
