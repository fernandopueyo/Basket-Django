from celery import shared_task
import requests
import json
from datetime import datetime
from django.db.models import Q, F, Sum

from calendar_basket.models import Calendar
from clasificacion.models import Clasificacion
from statistics_basketball.models import TeamStatistics

@shared_task
def actualizar_calendario():
    try:
        # Descargar datos de la federacion
        url_calendar_format = 'https://www.fbcv.es/wp-json/calendario/v1/id_grupo/{grupo}'
        url_clasificacion_format = "https://www.fbcv.es/wp-json/clasificaciones/v1/id_grupo/{grupo}"
        id_grupo = 83398
        calendar = requests.get(url_calendar_format.format(grupo=id_grupo)).json()
        calendar = json.loads(calendar)
        clasificacion = requests.get(url_clasificacion_format.format(grupo=id_grupo)).json()
        clasificacion = json.loads(clasificacion)["clasificacion"]

        # Actualizar calendario
        for jornadas in calendar:
            partidos = jornadas["Partidos"]
            for partido in partidos:
                partido = dict(partido)
                id_game = int(partido.get("IdPartido"))
                fecha_partido = partido.get("FechaPartido")
                fecha_partido = datetime.strptime(fecha_partido, "%d/%m/%Y %H:%M").date()
                resultado_local = int(partido.get("ResultadoLoc"))
                resultado_visitante = int(partido.get("ResultadoVis"))
                partido_model = Calendar.objects.get(id_game=id_game)
                partido_model.fecha_partido = fecha_partido
                partido_model.resultado_local = resultado_local
                partido_model.resultado_visitante = resultado_visitante
                partido_model.save()
        
        # Actualizar clasificacion
        for clasificado in clasificacion:
            clasificado = dict(clasificado)
            id_team = int(clasificado.get("IdEquipo"))
            posicion = int(clasificado.get("Posicion"))
            jugados = int(clasificado.get("Jugados"))
            puntos = int(clasificado.get("Puntos"))
            ganados = int(clasificado.get("Ganados"))
            perdidos = int(clasificado.get("Perdidos"))
            puntos_favor = int(clasificado.get("PuntosFavor"))
            puntos_contra = int(clasificado.get("PuntosContra"))
            clasificado_model = Clasificacion.objects.get(id_team=id_team)
            clasificado_model.posicion = posicion
            clasificado_model.jugados = jugados
            clasificado_model.puntos = puntos
            clasificado_model.ganados = ganados
            clasificado_model.perdidos = perdidos
            clasificado_model.puntos_favor = puntos_favor
            clasificado_model.puntos_contra = puntos_contra
            clasificado_model.save()

        # Cargar datos actualizados de la base de datos
        calendario = Calendar.objects.all()
        clasificacion = Clasificacion.objects.all()
        team_statistics = TeamStatistics.objects.all()

        # Actualizar estadisticas de equipo
        for row in team_statistics:
            # Columnas iguales de la clasificación
            row.posicion = clasificacion.get(id_team=row.id_team).posicion
            row.jugados = clasificacion.get(id_team=row.id_team).jugados
            row.ganados = clasificacion.get(id_team=row.id_team).ganados
            row.perdidos = clasificacion.get(id_team=row.id_team).perdidos

            # Valores de puntos generales
            if row.jugados != 0:
                row.puntos_favor = round(clasificacion.get(id_team=row.id_team).puntos_favor / row.jugados, 1)
                row.puntos_contra = round(clasificacion.get(id_team=row.id_team).puntos_contra / row.jugados, 1)
                row.dif_puntos = round(row.puntos_favor - row.puntos_contra, 1)
            else:
                row.puntos_favor = 0
                row.puntos_contra = 0
                row.dif_puntos = 0

            # Partidos ganados/perdidos
            partidos_equipo = calendario.filter(Q(id_equipo_local=row.id_team) | Q(id_equipo_visitante=row.id_team), Q(resultado_local__gt=0) | Q(resultado_visitante__gt=0))

            # Partidos en casa
            partidos_casa = partidos_equipo.filter(id_equipo_local=row.id_team)
            partidos_ganados_casa = partidos_casa.filter(resultado_local__gt=F('resultado_visitante'))
            partidos_perdidos_casa = partidos_casa.filter(resultado_local__lt=F('resultado_visitante'))
            row.c_jugados = partidos_casa.count()
            row.c_ganados = partidos_ganados_casa.count()
            row.c_perdidos = partidos_perdidos_casa.count()

            # Puntos generales en casa
            if row.c_jugados != 0:
                row.c_puntos_favor = round(partidos_casa.aggregate(Sum("resultado_local"))["resultado_local__sum"] / row.c_jugados, 1)
                row.c_puntos_contra = round(partidos_casa.aggregate(Sum("resultado_visitante"))["resultado_visitante__sum"] / row.c_jugados, 1)
                row.c_dif_puntos = round(row.c_puntos_favor - row.c_puntos_contra, 1)
            else:
                row.c_puntos_favor = 0
                row.c_puntos_contra = 0
                row.c_dif_puntos = 0

            # Puntos ganados y perdidos en casa
            if row.c_ganados != 0:
                row.c_g_puntos_favor = round(partidos_ganados_casa.aggregate(Sum("resultado_local"))["resultado_local__sum"] / row.c_ganados, 1)
                row.c_g_puntos_contra = round(partidos_ganados_casa.aggregate(Sum("resultado_visitante"))["resultado_visitante__sum"] / row.c_ganados, 1)
                row.c_g_dif_puntos = round(row.c_g_puntos_favor - row.c_g_puntos_contra, 1)
            else:
                row.c_g_puntos_favor = 0
                row.c_g_puntos_contra = 0
                row.c_g_dif_puntos = 0

            if row.c_perdidos != 0:
                row.c_p_puntos_favor = round(partidos_perdidos_casa.aggregate(Sum("resultado_local"))["resultado_local__sum"] / row.c_perdidos, 1)
                row.c_p_puntos_contra = round(partidos_perdidos_casa.aggregate(Sum("resultado_visitante"))["resultado_visitante__sum"] / row.c_perdidos, 1)
                row.c_p_dif_puntos = round(row.c_p_puntos_favor - row.c_p_puntos_contra, 1)
            else:
                row.c_p_puntos_favor = 0
                row.c_p_puntos_contra = 0
                row.c_p_dif_puntos = 0

            # Partidos fuera
            partidos_fuera = partidos_equipo.filter(id_equipo_visitante=row.id_team)
            partidos_ganados_fuera = partidos_fuera.filter(resultado_visitante__gt=F('resultado_local'))
            partidos_perdidos_fuera = partidos_fuera.filter(resultado_visitante__lt=F('resultado_local'))
            row.f_jugados = partidos_fuera.count()
            row.f_ganados = partidos_ganados_fuera.count()
            row.f_perdidos = partidos_perdidos_fuera.count()

            # Puntos generales fuera
            if row.f_jugados != 0:
                row.f_puntos_favor = round(partidos_fuera.aggregate(Sum("resultado_visitante"))["resultado_visitante__sum"] / row.f_jugados, 1)
                row.f_puntos_contra = round(partidos_fuera.aggregate(Sum("resultado_local"))["resultado_local__sum"] / row.f_jugados, 1)
                row.f_dif_puntos = round(row.f_puntos_favor - row.f_puntos_contra, 1)
            else:
                row.f_puntos_favor = 0
                row.f_puntos_contra = 0
                row.f_dif_puntos = 0

            # Puntos ganados y perdidos fuera
            if row.f_ganados != 0:
                row.f_g_puntos_favor = round(partidos_ganados_fuera.aggregate(Sum("resultado_visitante"))["resultado_visitante__sum"] / row.f_ganados, 1)
                row.f_g_puntos_contra = round(partidos_ganados_fuera.aggregate(Sum("resultado_local"))["resultado_local__sum"] / row.f_ganados, 1)
                row.f_g_dif_puntos = round(row.f_g_puntos_favor - row.f_g_puntos_contra, 1)
            else:
                row.f_g_puntos_favor = 0
                row.f_g_puntos_contra = 0
                row.f_g_dif_puntos = 0

            if row.f_perdidos != 0:
                row.f_p_puntos_favor = round(partidos_perdidos_fuera.aggregate(Sum("resultado_visitante"))["resultado_visitante__sum"] / row.f_perdidos, 1)
                row.f_p_puntos_contra = round(partidos_perdidos_fuera.aggregate(Sum("resultado_local"))["resultado_local__sum"] / row.f_perdidos, 1)
                row.f_p_dif_puntos = round(row.f_p_puntos_favor - row.f_p_puntos_contra, 1)
            else:
                row.f_p_puntos_favor = 0
                row.f_p_puntos_contra = 0
                row.f_p_dif_puntos = 0

            # Puntos ganados y perdidos total
            if row.ganados != 0:
                row.g_puntos_favor = round((
                    (partidos_ganados_casa.aggregate(Sum("resultado_local"))["resultado_local__sum"] or 0) +
                    (partidos_ganados_fuera.aggregate(Sum("resultado_visitante"))["resultado_visitante__sum"] or 0)
                ) / row.ganados, 1)
                row.g_puntos_contra = round((
                    (partidos_ganados_casa.aggregate(Sum("resultado_visitante"))["resultado_visitante__sum"] or 0) +
                    (partidos_ganados_fuera.aggregate(Sum("resultado_local"))["resultado_local__sum"] or 0)
                ) / row.ganados, 1)
                row.g_dif_puntos = round(row.g_puntos_favor - row.g_puntos_contra, 1)
            else:
                row.g_puntos_favor = 0
                row.g_puntos_contra = 0
                row.g_dif_puntos = 0
            
            if row.perdidos != 0:
                row.p_puntos_favor = round((
                    (partidos_perdidos_casa.aggregate(Sum("resultado_local"))["resultado_local__sum"] or 0) +
                    (partidos_perdidos_fuera.aggregate(Sum("resultado_visitante"))["resultado_visitante__sum"] or 0)
                ) / row.perdidos, 1)
                row.p_puntos_contra = round((
                    (partidos_perdidos_casa.aggregate(Sum("resultado_visitante"))["resultado_visitante__sum"] or 0) +
                    (partidos_perdidos_fuera.aggregate(Sum("resultado_local"))["resultado_local__sum"] or 0)
                ) / row.perdidos, 1)
                row.p_dif_puntos = round(row.p_puntos_favor - row.p_puntos_contra, 1)
            else:
                row.p_puntos_favor = 0
                row.p_puntos_contra = 0
                row.p_dif_puntos = 0
            
            # Guardar cambios
            row.save()
        
        # Calcular posición en casa y fuera
        team_statistics = TeamStatistics.objects.all()
        equipos_casa = team_statistics.filter(c_jugados__gt=0).order_by("-c_ganados", "-c_dif_puntos", "-c_puntos_favor")
        equipos_fuera = team_statistics.filter(f_jugados__gt=0).order_by("-f_ganados", "-f_dif_puntos", "-f_puntos_favor")

        posicion_casa = 1
        for row in equipos_casa:
            row.c_posicion = posicion_casa
            row.save()
            posicion_casa += 1
        
        posicion_fuera = 1    
        for row in equipos_fuera:
            row.f_posicion = posicion_fuera
            row.save()
            posicion_fuera += 1

        print("Calendario y clasificacion actualizados correctamente")

        return

    except Exception as e:
        print("Error:", e)
        return
