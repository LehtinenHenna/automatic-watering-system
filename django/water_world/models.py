from djongo import models

class Config(models.Model):
  class SystemMode(models.IntegerChoices):
    SENSOR_MODE = 1
    TIMER_MODE = 2

  enable_system = models.BooleanField("System ON",)
  system_mode = models.IntegerField(choices=SystemMode.choices)
  seconds_to_pump = models.FloatField("Seconds pumped per pump activation",)
  sensor_read_interval_hours = models.FloatField("Sensor read interval in sensor mode (hours)",)
  watering_interval_hours = models.FloatField("Watering interval in timer mode (hours)")

  def __str__(self):
    return "System Config"


class WaterPump(models.Model):
  pump_activated = models.DateTimeField("Pump activation timestamp", primary_key=True,)
  pump_stopped = models.DateTimeField("Pump stopping timestamp",)

  class Meta:
    verbose_name_plural = "Pump activations"

  def __str__(self):
    return self.pump_activated


class Event(models.Model):
  message = models.TextField("Event message",)
  event_type = models.CharField("Event type", max_length=100)
  event_time = models.DateTimeField("Event timestamp", primary_key=True,)

  def __str__(self):
    return self.message
