from rest_framework import viewsets, permissions
from clasificacion.models import Clasificacion
from .serializers import ClasificacionSerializer
from django.db.models import Q
from django_filters import rest_framework as filters


class ClasificacionFilter(filters.FilterSet):
    posicion = filters.NumberFilter(field_name='posicion')
    id_equipo = filters.NumberFilter(field_name='id_team')

    class Meta:
        model = Clasificacion
        fields = ['posicion', 'id_equipo']


class ClasificacionViewSet(viewsets.ModelViewSet):
    queryset = Clasificacion.objects.all()
    serializer_class = ClasificacionSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ClasificacionFilter