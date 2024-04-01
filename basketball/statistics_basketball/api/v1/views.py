from rest_framework import viewsets, permissions
from statistics_basketball.models import Statistics, TeamStatistics
from .serializers import StatisticsSerializer, TeamStatisticsSerializer
from django_filters import rest_framework as filters


class StatisticsFilter(filters.FilterSet):
    id_partido = filters.NumberFilter(field_name='id_game')
    id_equipo = filters.NumberFilter(field_name='id_team')
    id_jugador = filters.NumberFilter(field_name='id_player')

    class Meta:
        model = Statistics
        fields = ['id_partido', 'id_equipo', 'id_jugador']

class TeamStatisticsFilter(filters.FilterSet):
    id_equipo = filters.NumberFilter(field_name='id_team')

    class Meta:
        model = TeamStatistics
        fields = ['id_equipo']

class StatisticsViewSet(viewsets.ModelViewSet):
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = StatisticsFilter

class TeamStatisticsViewSet(viewsets.ModelViewSet):
    queryset = TeamStatistics.objects.all()
    serializer_class = TeamStatisticsSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = TeamStatisticsFilter