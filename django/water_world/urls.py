"""Determine URLs for Water World app."""

from django.urls import path

from . import views

# Namespace to be used in the views templates
app_name = "water_world"

urlpatterns = [
    path("config/", views.ConfigView.as_view(), name="config"),
]
