from django.conf import settings
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required

from .models import Calendar, Teams

class CalendarAdmin(admin.ModelAdmin):
    list_display = ('num_jornada', 'equipo_local', 'equipo_visitante')
    list_filter = ('num_jornada',)
    search_fields = ('equipo_local', 'equipo_visitante') 

admin.site.register(Calendar, CalendarAdmin)

admin.site.login = staff_member_required(
    admin.site.login, login_url=settings.LOGIN_URL
)
