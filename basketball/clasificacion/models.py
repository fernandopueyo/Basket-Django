from django.db import models
from calendar_basket.models import Teams

class Clasificacion(models.Model):
    id_team = models.OneToOneField(Teams, models.DO_NOTHING, db_column='id_team', primary_key=True)
    posicion = models.BigIntegerField(blank=True, null=True)
    jugados = models.BigIntegerField(blank=True, null=True)
    puntos = models.BigIntegerField(blank=True, null=True)
    ganados = models.BigIntegerField(blank=True, null=True)
    perdidos = models.BigIntegerField(blank=True, null=True)
    puntos_favor = models.BigIntegerField(blank=True, null=True)
    puntos_contra = models.BigIntegerField(blank=True, null=True)
    racha = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'clasificacion'