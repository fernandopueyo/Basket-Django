from django.db import models
from calendar_basket.models import Calendar, Teams
from perfil.models import Players


class Statistics(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_team = models.ForeignKey(Teams, models.DO_NOTHING, db_column='id_team', blank=True, null=True)
    id_player = models.ForeignKey(Players, models.DO_NOTHING, db_column='id_player', blank=True, null=True)
    id_game = models.ForeignKey(Calendar, models.DO_NOTHING, db_column='id_game', blank=True, null=True)
    mins = models.BigIntegerField(blank=True, null=True, default=0)
    fgm = models.BigIntegerField(blank=True, null=True, default=0)
    fga = models.BigIntegerField(blank=True, null=True, default=0)
    fgperc = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=0)
    threepm = models.BigIntegerField(blank=True, null=True, default=0)
    threepa = models.BigIntegerField(blank=True, null=True, default=0)
    threepperc = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=0)
    ftm = models.BigIntegerField(blank=True, null=True, default=0)
    fta = models.BigIntegerField(blank=True, null=True, default=0)
    ftperc = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=0)
    reb = models.BigIntegerField(blank=True, null=True, default=0)
    ast = models.BigIntegerField(blank=True, null=True, default=0)
    stl = models.BigIntegerField(blank=True, null=True, default=0)
    blk = models.BigIntegerField(blank=True, null=True, default=0)
    turnover = models.BigIntegerField(blank=True, null=True, default=0)
    pf = models.BigIntegerField(blank=True, null=True, default=0)
    pts = models.BigIntegerField(blank=True, null=True, default=0)
    win = models.BooleanField(blank=True, null=True, default=False)

    class Meta:
        managed = True        
        db_table = 'statistics'
        unique_together = (('id_game', 'id_player', 'id_team'),)


class ShotStatistics(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_team = models.ForeignKey(Teams, models.DO_NOTHING, db_column='id_team', blank=True, null=True)
    id_player = models.ForeignKey(Players, models.DO_NOTHING, db_column='id_player', blank=True, null=True)
    id_game = models.ForeignKey(Calendar, models.DO_NOTHING, db_column='id_game', blank=True, null=True)
    id_statistics = models.ForeignKey(Statistics, models.DO_NOTHING, db_column='id_statistics', blank=True, null=True)
    x = models.BigIntegerField(blank=True, null=True)
    y = models.BigIntegerField(blank=True, null=True)
    made = models.BooleanField(blank=True, null=True, default=False)
    threep = models.BooleanField(blank=True, null=True, default=False)

    class Meta:
        managed = True        
        db_table = 'shot_statistics'
        

class TeamStatistics(models.Model):
    id_team = models.BigIntegerField(primary_key=True)
    team = models.TextField(blank=True, null=True)
    posicion = models.BigIntegerField(blank=True, null=True)
    jugados = models.BigIntegerField(blank=True, null=True)
    ganados = models.BigIntegerField(blank=True, null=True)
    perdidos = models.BigIntegerField(blank=True, null=True)
    puntos_favor = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    puntos_contra = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    dif_puntos = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    g_puntos_favor = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    g_puntos_contra = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    g_dif_puntos = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    p_puntos_favor = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    p_puntos_contra = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    p_dif_puntos = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    c_posicion = models.BigIntegerField(blank=True, null=True)
    c_jugados = models.BigIntegerField(blank=True, null=True)
    c_ganados = models.BigIntegerField(blank=True, null=True)
    c_perdidos = models.BigIntegerField(blank=True, null=True)
    c_puntos_favor = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    c_puntos_contra = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    c_dif_puntos = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    c_g_puntos_favor = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    c_g_puntos_contra = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    c_g_dif_puntos = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    c_p_puntos_favor = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    c_p_puntos_contra = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    c_p_dif_puntos = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    f_posicion = models.BigIntegerField(blank=True, null=True)
    f_jugados = models.BigIntegerField(blank=True, null=True)
    f_ganados = models.BigIntegerField(blank=True, null=True)
    f_perdidos = models.BigIntegerField(blank=True, null=True)
    f_puntos_favor = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    f_puntos_contra = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    f_dif_puntos = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    f_g_puntos_favor = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    f_g_puntos_contra = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    f_g_dif_puntos = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    f_p_puntos_favor = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    f_p_puntos_contra = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    f_p_dif_puntos = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'team_statistics'

