from rest_framework import serializers
from perfil.models import Players

class PlayersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Players
        fields = ['id_team', 'dorsal', 'first_name', 'last_name']