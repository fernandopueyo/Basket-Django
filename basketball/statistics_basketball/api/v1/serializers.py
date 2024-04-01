from rest_framework import serializers
from statistics_basketball.models import Statistics, TeamStatistics

class StatisticsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Statistics
        fields = ['id_team', 'id_player', 'id_game', 'mins', 'fgm', 'fga', 'fgperc', 'threepm', 'threepa', 'threepperc', 'ftm', 'fta', 'ftperc', 'reb', 'ast', 'stl', 'blk', 'turnover', 'pf', 'pts', 'win']

class TeamStatisticsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TeamStatistics
        fields = ['id_team', 'team', 'posicion', 'jugados', 'ganados', 'perdidos', 'puntos_favor', 'puntos_contra', 'dif_puntos', 'g_puntos_favor', 'g_puntos_contra', 'g_dif_puntos', 'p_puntos_favor', 'p_puntos_contra', 'p_dif_puntos',
                'c_posicion', 'c_jugados', 'c_ganados', 'c_perdidos', 'c_puntos_favor', 'c_puntos_contra', 'c_dif_puntos', 'c_g_puntos_favor', 'c_g_puntos_contra', 'c_g_dif_puntos', 'c_p_puntos_favor', 'c_p_puntos_contra', 'c_p_dif_puntos',
                'f_posicion', 'f_jugados', 'f_ganados', 'f_perdidos', 'f_puntos_favor', 'f_puntos_contra', 'f_dif_puntos', 'f_g_puntos_favor', 'f_g_puntos_contra', 'f_g_dif_puntos', 'f_p_puntos_favor', 'f_p_puntos_contra', 'f_p_dif_puntos',]
        

