from django.db.models import Q

from .models import Calendar, Teams

from .forms import FilterForm


# Vista calendar
def obtener_calendario( equipo, jornada ):
    filtrar_equipo = Q(id_equipo_local=equipo) | Q(id_equipo_visitante=equipo)
    filtrar_jornada = Q(num_jornada=jornada)
    if equipo and not jornada:
        calendario = Calendar.objects.filter(filtrar_equipo)
    elif not equipo and jornada:
        calendario = Calendar.objects.filter(filtrar_jornada)
    elif equipo and jornada:
        calendario = Calendar.objects.filter(filtrar_equipo, filtrar_jornada)
    else:
        calendario = Calendar.objects.all()
    return calendario.order_by("num_jornada").order_by("fecha_partido") 

def obtener_equipos():
    equipos = Teams.objects.all()
    return equipos

def ordenar_calendario(calendario):
    calendario_por_jornada = {}
    for partido in calendario:
        num_jornada = partido.num_jornada
        if num_jornada not in calendario_por_jornada:
            calendario_por_jornada[num_jornada] = []
        calendario_por_jornada[num_jornada].append(partido)
    return calendario_por_jornada

def aplicar_filtro_calendario(calendario, form):
    if form.is_valid():
        equipo_filtro = form.cleaned_data['equipo']
        jornada_filtro = form.cleaned_data['jornada']

        if equipo_filtro:
            calendario = calendario.filter(id_equipo_local=equipo_filtro.id_team) | calendario.filter(id_equipo_visitante=equipo_filtro.id_team)

        if jornada_filtro:
            calendario = calendario.filter(num_jornada=jornada_filtro)
    return calendario

def calendar_view(request):
    form = FilterForm(request.GET)
    equipo_fitro = form.cleaned_data['equipo'].id_team if form.is_valid() and form.cleaned_data['equipo'] else None
    jornada_filtro = form.cleaned_data['jornada'] if form.is_valid() and form.cleaned_data['jornada'] else None
    calendario_por_jornada = ordenar_calendario(obtener_calendario(equipo_fitro, jornada_filtro))
    # calendario_por_jornada = aplicar_filtro_calendario(calendario, form)
    context = {
        'calendario_por_jornada': calendario_por_jornada,
        'form': form,
    }
    return context


# Statistics
def partidos_jugador(calendario, player):
    partidos = calendario.filter(Q(id_equipo_local=player.id_team.id_team) | Q(id_equipo_visitante=player.id_team.id_team))
    return partidos

def obtener_partido(id_game):
    partido = Calendar.objects.get(id_game=id_game)
    return partido