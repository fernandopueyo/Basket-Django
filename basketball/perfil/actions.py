from statistics_basketball.actions import player_login

from .models import Players
from .forms import PlayerForm

# Vista complete_player_profile
def form_complete_profile(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False) 
            player.user = request.user 
            player.save() 
            return None

    else:
        form = PlayerForm()

    return form

def v_complete_player_profile_view(request):
    player = player_login(request)
    if player and player.is_complete():
        return None
    form = form_complete_profile(request)
    if not form:
        return None
    context = {
        'form': form,
    }

    return context

# Vista perfil
def form_profile(request, player):
    if request.method == 'POST':
        player_form = PlayerForm(request.POST, instance=player)
        if player_form.is_valid():
            player_form.save()

    else:
        player_form = PlayerForm(instance=player)

    return player_form

def v_profile(request):
    player = player_login(request)
    if not player or not player.is_complete():
        return None
    player_form = form_profile(request, player)
    context = {
        'user': request.user,
        'player': player,
        'player_form': player_form,
    }

    return context