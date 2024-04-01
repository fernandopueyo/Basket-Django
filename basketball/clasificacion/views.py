from django.shortcuts import render

from .actions import clasificacion_view


def clasificacion(request):
    context = clasificacion_view()

    return render(request, 'clasificacion/clasificacion.html', context)