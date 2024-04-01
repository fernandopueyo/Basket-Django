from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'statistics', views.StatisticsViewSet)
router.register(r'team-statistics', views.TeamStatisticsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
