from django.shortcuts import render

from .actions import calendar_view


def calendar(request):
    context = calendar_view(request)

    return render(request, 'calendar_basket/calendar.html', context)
