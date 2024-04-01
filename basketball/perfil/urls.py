from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


app_name = "perfil"

urlpatterns = [
    path('complete-player-profile/', views.complete_player_profile_view, name='complete_player_profile'),
    path('', views.perfil, name='perfil'),
]