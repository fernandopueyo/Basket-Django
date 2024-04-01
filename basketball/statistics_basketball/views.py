from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .actions import v_view_statistics, v_statistics, v_add_statistics, v_bokeh_shot_stats, v_bokeh_player_stats, v_team_statistics


@login_required
def view_statistics(request, id_game):
    context = v_view_statistics(request, id_game)
    if context is None:
        return redirect('perfil:complete_player_profile')
    return render(request, 'statistics_basketball/statistics_game.html', context)


@login_required
def statistics(request):
    context = v_statistics(request)
    if context is None:
        return redirect('perfil:complete_player_profile')

    return render(request, 'statistics_basketball/statistics.html', context)


@login_required
def add_statistics(request, id_game):
    context = v_add_statistics(request, id_game)
    if context is None:
        return redirect('perfil:complete_player_profile')
    if isinstance(context, dict):
        print("meter datos")
        return render(request, 'statistics_basketball/add_statistics.html', context)
    else:
        print("redirigir")
        return redirect('statistics:statistics_game', id_game=id_game)


@login_required
def bokeh_shot_stats(request, id_game):
    context = v_bokeh_shot_stats(request, id_game)
    if context is None:
        return redirect('perfil:complete_player_profile')

    return render(request, 'statistics_basketball/shot_plot.html', context)


@login_required
def bokeh_player_stats(request):
    context = v_bokeh_player_stats(request)
    if  not context:
        return redirect('perfil:complete_player_profile')

    return render(request, 'statistics_basketball/player_stats.html', context)


@login_required
def team_statistics(request):
    context = v_team_statistics(request)

    return render(request, 'statistics_basketball/team_statistics.html', context)

