from django.db import models
from django.contrib.auth.models import User


class Calendar(models.Model):
    num_jornada = models.BigIntegerField()
    id_game = models.BigIntegerField(primary_key=True)
    id_equipo_local = models.BigIntegerField()
    id_equipo_visitante = models.BigIntegerField()
    equipo_local = models.CharField(max_length=50)
    equipo_visitante = models.CharField(max_length=50)
    fecha_partido = models.DateField()
    resultado_local = models.BigIntegerField(blank=True, null=True)
    resultado_visitante = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'calendar'
        ordering = ['num_jornada']


class Teams(models.Model):
    id = models.BigIntegerField()
    name = models.TextField()
    id_team = models.BigIntegerField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'teams'
    
    def __str__(self):
        return self.name
    


