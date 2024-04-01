from rest_framework import serializers
from clasificacion.models import Clasificacion

class ClasificacionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Clasificacion
        fields = ['posicion', 'jugados', 'puntos', 'ganados', 'perdidos', 'puntos_favor', 'puntos_contra', 'racha']