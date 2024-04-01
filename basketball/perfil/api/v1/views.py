from rest_framework import viewsets, permissions
from perfil.models import Players
from .serializers import PlayersSerializer
from django_filters import rest_framework as filters


class PlayersFilter(filters.FilterSet):
    id_equipo = filters.NumberFilter(field_name='id_team')

    class Meta:
        model = Players
        fields = ['id_equipo']


class PlayersViewSet(viewsets.ModelViewSet):
    queryset = Players.objects.all()
    serializer_class = PlayersSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PlayersFilter