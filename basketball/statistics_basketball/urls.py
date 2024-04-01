from django.urls import path
from . import views

app_name = "statistics"

urlpatterns = [
    path("", views.statistics, name="statistics"),
    path("<int:id_game>/", views.view_statistics, name="statistics_game"),
    path("add/<int:id_game>/", views.add_statistics, name="add_statistics"),
    path("shot_plot/<int:id_game>/", views.bokeh_shot_stats, name="shot_plot"),
    path("playerstats/", views.bokeh_player_stats, name="player_stats"),
    path("team_statistics/", views.team_statistics, name="team_statistics"),
]
