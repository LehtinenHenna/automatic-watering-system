from django.db import models


class Config(models.Model):
    """Config model."""

    config_text = models.CharField(max_length=200)

    def __str__(self):
        return str(self.config_text)
