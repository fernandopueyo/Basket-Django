from rest_framework import serializers
from calendar_basket.models import Calendar, Teams

class CalendarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Calendar
        fields = ['num_jornada', 'equipo_local', 'equipo_visitante', 'fecha_partido', 'resultado_local', 'resultado_visitante']

class TeamsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Teams
        fields = ['name', 'id_team']