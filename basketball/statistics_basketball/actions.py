from django.shortcuts import redirect, get_object_or_404
from django.utils.html import format_html

from calendar_basket.models import Calendar
from calendar_basket.actions import obtener_calendario, partidos_jugador
from perfil.models import Players
from statistics_basketball.models import Statistics, ShotStatistics, TeamStatistics
from statistics_basketball.forms import StatisticsForm, ShotForm

from bokeh.embed import server_document
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# Vista view_statistics
def player_login(request):
    user = request.user
    try:
        player = Players.objects.get(user=user)
    except Players.DoesNotExist:
        player = None
    if not player or not player.is_complete():
        return None

    return player

def obtener_partido(id_game):
    partido = get_object_or_404(Calendar, id_game=id_game)
    return partido

def obtener_estadisticas_local_visitante(partido):
    estadisticas_local = Statistics.objects.filter(id_game=partido.id_game, id_team=partido.id_equipo_local).select_related('id_player')
    estadisticas_visitante = Statistics.objects.filter(id_game=partido.id_game, id_team=partido.id_equipo_visitante).select_related('id_player')
    return estadisticas_local, estadisticas_visitante

def estadisticas_vista(estadisticas_local, estadisticas_visitante):
    for estadistica in estadisticas_local:
        estadistica.fgperc *= 100
        estadistica.threepperc *= 100
        estadistica.ftperc *= 100
    for estadistica in estadisticas_visitante:
        estadistica.fgperc *= 100
        estadistica.threepperc *= 100
        estadistica.ftperc *= 100
    return estadisticas_local, estadisticas_visitante

def v_view_statistics(request, id_game):
    player = player_login(request)
    if not player or not player.is_complete():
        return None
    partido = obtener_partido(id_game)
    estadisticas_local, estadisticas_visitante = obtener_estadisticas_local_visitante(partido)
    estadisticas_local, estadisticas_visitante = estadisticas_vista(estadisticas_local, estadisticas_visitante)
    context = {
        'partido': partido,
        'estadisticas_local': estadisticas_local,
        'estadisticas_visitante': estadisticas_visitante,
        'player': player,
    }
    return context

# Vista statistics
def v_statistics(request):
    player = player_login(request)
    if not player or not player.is_complete():
        return None
    calendario = obtener_calendario(equipo=player.id_team.id_team,jornada=None)
    partidos = partidos_jugador(calendario, player)
    context = {
        'partidos': partidos,
    }
    return context

# Vista add_statistics
def estadisticas_jugador_partido(player, id_game):
    statistics_player_game = Statistics.objects.filter(id_game=id_game, id_player=player.id).first()
    return statistics_player_game

def v_add_statistics(request, id_game):
    player = player_login(request)
    if not player or not player.is_complete():
        return None
    
    game = obtener_partido(id_game)
    statistics_player_game = estadisticas_jugador_partido(player, id_game)

    if request.method == 'POST':
        if statistics_player_game and statistics_player_game.id_player == player and statistics_player_game.id_game == game:
            form = StatisticsForm(request.POST, instance=statistics_player_game)
            if form.is_valid():
                statistics = form.save(commit=False) 
                statistics.ftperc = statistics.ftm / statistics.fta if statistics.fta > 0 else 0
                statistics.pts = statistics.fgm * 2 + statistics.threepm * 3 + statistics.ftm
                if statistics_player_game.id_game.id_equipo_local == player.id_team.id_team:
                    if statistics_player_game.id_game.resultado_local > statistics_player_game.id_game.resultado_visitante:
                        statistics.win = True
                    else:
                        statistics.win = False
                elif statistics_player_game.id_game.id_equipo_visitante == player.id_team.id_team:
                    if statistics_player_game.id_game.resultado_visitante > statistics_player_game.id_game.resultado_local:
                        statistics.win = True
                    else:
                        statistics.win = False
                shot_statistics = ShotStatistics.objects.filter(id_player = player, id_game = game)
                if shot_statistics:
                    for shot in shot_statistics:
                        shot.id_statistics = statistics
                        shot.save()
                statistics.save() 
                return 'redirect'
        else:
            form = StatisticsForm(request.POST)
            if form.is_valid():
                statistics = form.save(commit=False)  
                statistics.id_player = player
                statistics.id_team = player.id_team
                statistics.id_game = game
                statistics.ftperc = statistics.ftm / statistics.fta if statistics.fta > 0 else 0
                statistics.pts = statistics.fgm * 2 + statistics.threepm * 3 + statistics.ftm
                shot_statistics = ShotStatistics.objects.filter(id_player = player, id_game = game)
                if shot_statistics:
                    for shot in shot_statistics:
                        shot.id_statistics = statistics
                        shot.save()
                statistics.save() 
                return 'redirect'

    else:
        form = StatisticsForm(instance=statistics_player_game if statistics_player_game else None)
    
    context = {
        'form': form,
    }

    return context

# Vista bokeh_shot_stats
def v_bokeh_shot_stats(request, id_game):
    player = player_login(request)
    if not player or not player.is_complete():
        return None
    url_bokeh = "http://localhost:5006/bokeh_basket"
    arguments = {'id_game': id_game, 'id_player': player.id}
    script = server_document(url_bokeh, arguments=arguments)
    context = {
        'script': script,
        'id_game': id_game,
    }

    return context

# Vista bokeh_player_stats
def obtener_shots(player):
    shots = ShotStatistics.objects.filter(id_player=player.id).select_related('id_statistics')
    return shots

def shots_form(request, shots):
    if request.method == 'POST':
        form = ShotForm(request.POST)
        if form.is_valid():
            win = form.cleaned_data['win']
            if win != '':
                win = win == 'True'
                shots = shots.filter(id_statistics__win=win)
            else:
                shots = shots
            made = form.cleaned_data['made']
            if made != '':
                made = made == 'True'
                shots = shots.filter(made=made)
            else:
                shots = shots
    else:
        form = ShotForm()
        shots = shots
    return form, shots

class Img():
    def __init__(self):
            self.image = None

    def from_figure(self, input: plt.Figure):
        plot_file = BytesIO()
        input.savefig(plot_file, format='png')
        self.image = base64.b64encode(plot_file.getvalue()).decode()

    def to_html(self):
        return format_html('<img src="data:image/png;base64,{}">', self.image)


def player_stats_crear_imagenes(shots):
    # Extrae las posiciones de los tiros
    x = [shot.x for shot in shots]
    y = [shot.y for shot in shots]
    made = ["Anotado" if shot.made else "Fallado" for shot in shots]

    # Crear un DataFrame de Pandas con las coordenadas
    df = pd.DataFrame({'coordenada_x': x, 'coordenada_y': y, 'made': made})

    # Crear el gráfico
    fig1, ax1 = plt.subplots(figsize=(6, 6))

    ax1.axis('off')
    background_img = plt.imread("static/images/halfcourt.png")  

    ax1.imshow(background_img, extent=[0, 500, 0, 500], alpha=0.7)

    # Define los colores de inicio, medio y final
    start_color = (154/255, 141/255, 153/255)
    middle_color = (112/255, 68/255, 104/255)
    end_color = (248/255, 157/255, 37/255)

    #f89d25

    # Crea la paleta de colores
    colors = [start_color, middle_color, end_color]
    cmap = sns.blend_palette(colors, as_cmap=True)
    # cmap = sns.color_palette("ch:s=-.2,r=.6", as_cmap=True)
    sns.kdeplot(data=df, x='coordenada_x', y='coordenada_y', cmap=cmap, fill=True, levels=[0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], alpha=0.8, ax=ax1, warn_singular=False)

    # Ajustar tamaño y eliminar borde blanco
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.xlim(0, 500)
    plt.ylim(0, 500)
    plt.gca().set_axis_off()
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0, 0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())

    # Uso de la Helperclass para convertir el gráfico a imagen, almacenar en BytesIO y codificar en base64
    img1 = Img()
    img1.from_figure(fig1)
    div1 = img1.to_html()    

    # Crear el gráfico
    fig2, ax2 = plt.subplots(figsize=(6, 6))

    ax2.axis('off')
    background_img = plt.imread("static/images/halfcourt.png")  

    ax2.imshow(background_img, extent=[0, 500, 0, 500], alpha=0.7)

    # Crear un diccionario para mapear los valores de 'made' a los colores deseados
    palette = {"Anotado": "green", "Fallado": "red"}

    # Crear un diccionario para mapear los valores de 'made' a los marcadores deseados
    markers = {"Anotado": "o", "Fallado": "X"}

    # Crear un diccionario para mapear los valores de 'made' a los tamaños deseados
    sizes = {"Anotado": 100, "Fallado": 100}

    sns.scatterplot(data=df, x='coordenada_x', y='coordenada_y', hue='made', palette=palette, size='made', sizes=sizes, style='made', markers=markers, alpha=0.8, ax=ax2)

    # Modificar la leyenda
    legend = ax2.get_legend()
    if legend:
        legend.set_title('')
        legend.get_frame().set_alpha(0.5)

    # Ajustar tamaño y eliminar borde blanco
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.xlim(0, 500)
    plt.ylim(0, 500)
    plt.gca().set_axis_off()
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0, 0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())

    # Uso de la Helperclass para convertir el gráfico a imagen, almacenar en BytesIO y codificar en base64
    img2 = Img()
    img2.from_figure(fig2)
    div2 = img2.to_html()  

    return div1, div2

def obtener_estadisticas(player):
    estadisticas = Statistics.objects.filter(id_player=player.id).select_related('id_game').order_by('id_game__fecha_partido')
    return estadisticas

def player_stats_crear_estadisticas(estadisticas):
    for estadistica in estadisticas:
        estadistica.fgperc *= 100
        estadistica.threepperc *= 100
        estadistica.ftperc *= 100

    # Convierte las estadísticas en un DataFrame de pandas
    df_statistics = pd.DataFrame.from_records(estadisticas.values())
    df_statistics[["fgperc","threepperc","ftperc"]] *= 100

    columns = ['mins', 'fgm', 'fga', 'fgperc', 'threepm', 'threepa', 'threepperc', 'ftm', 'fta', 'ftperc', 'reb', 'ast', 'stl', 'blk', 'turnover', 'pf', 'pts']

    estadisticas_medias = df_statistics[columns].mean()
    estadisticas_medias_victoria = df_statistics[df_statistics["win"]][columns].mean()
    estadisticas_medias_derrota = df_statistics[df_statistics["win"] != True][columns].mean()

    return estadisticas, estadisticas_medias, estadisticas_medias_victoria, estadisticas_medias_derrota

def v_bokeh_player_stats(request):
    player = player_login(request)
    if not player or not player.is_complete():
        return None
    estadisticas = obtener_estadisticas(player)
    if not estadisticas:
        context = {
            'faltan_estadisticas': 'faltan_estadisticas'
        }
        return context
    
    estadisticas, estadisticas_medias, estadisticas_medias_victoria, estadisticas_medias_derrota = player_stats_crear_estadisticas(estadisticas)

    shots = obtener_shots(player)
    if not shots:
        context = {
            'estadisticas': estadisticas,
            'estadisticas_medias': estadisticas_medias,
            'estadisticas_medias_victoria': estadisticas_medias_victoria,
            'estadisticas_medias_derrota': estadisticas_medias_derrota,
            'faltan_tiros': 'faltan_tiros',
        }
        return context

    form, shots = shots_form(request, shots)
    div1, div2 = player_stats_crear_imagenes(shots)
    context = {
        'div1': div1,
        'div2': div2,
        'estadisticas': estadisticas,
        'estadisticas_medias': estadisticas_medias,
        'estadisticas_medias_victoria': estadisticas_medias_victoria,
        'estadisticas_medias_derrota': estadisticas_medias_derrota,
        'form': form,
    }

    return context

# Vista team_statistics
def v_team_statistics(request):
    team_statistics = TeamStatistics.objects.all().order_by('posicion')
    team_statistics_casa = team_statistics.order_by('c_posicion')
    team_statistics_fuera = team_statistics.order_by('f_posicion')

    context = {
        'team_statistics': team_statistics,
        'team_statistics_casa': team_statistics_casa,
        'team_statistics_fuera': team_statistics_fuera,
    }

    return context