from rest_framework import viewsets, permissions
from calendar_basket.models import Calendar, Teams
from .serializers import CalendarSerializer, TeamsSerializer
from django.db.models import Q
from django_filters import rest_framework as filters


class CalendarFilter(filters.FilterSet):
    num_jornada = filters.NumberFilter(field_name='num_jornada')
    id_equipo = filters.NumberFilter(method='filter_id_equipo')

    def filter_id_equipo(self, queryset, name, value):
        return queryset.filter(Q(id_equipo_local=value) | Q(id_equipo_visitante=value))

    class Meta:
        model = Calendar
        fields = ['num_jornada', 'id_equipo']


class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CalendarFilter

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Teams.objects.all()
    serializer_class = TeamsSerializer
    permission_classes = [permissions.AllowAny]