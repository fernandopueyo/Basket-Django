from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .actions import v_complete_player_profile_view, v_profile

@login_required  
def complete_player_profile_view(request):
    context = v_complete_player_profile_view(request)
    if not context:
        return redirect('index')

    return render(request, 'perfil/complete_player_profile.html', context)

@login_required
def perfil(request):
    context = v_profile(request)
    if not context:
        return redirect('perfil:complete_player_profile')

    return render(request, 'perfil/perfil.html', context)