"""Determine URLs for Water World app."""

from django.urls import path

from . import views

# Namespace to be used in the views templates
app_name = "water_world"

urlpatterns = [
    path('events/', views.EventView.as_view(), name='events'),
    path('pump/', views.PumpView.as_view(), name='pump'),
]
