from django.urls import path
from . import views

app_name = "calendar"

urlpatterns = [
    path("", views.calendar, name='calendar_basket'),
]