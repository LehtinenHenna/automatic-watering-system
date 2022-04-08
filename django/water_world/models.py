from django.db import models

class Config(models.Model):
  enable_system = models.BooleanField("System on/off switch",)
  liters_to_pump = models.FloatField("Liters pumped per pump activation",)
  sensor_read_interval_hours = models.IntegerField("Sensor read interval in hours",)


class WaterPump(models.Model):
  pump_activated = models.DateTimeField("Pump activation timestamp", blank=True, null=True,)
  pump_stopped = models.DateTimeField("Pump stopping timestamp", blank=True, null=True,)
