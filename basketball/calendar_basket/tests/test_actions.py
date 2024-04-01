from django.test import TestCase
from calendar_basket.models import Calendar, Teams
from calendar_basket.actions import obtener_calendario

class CalendarActionsTestCase(TestCase):
    def setUp(self):
        Calendar.objects.create(num_jornada=1, id_game=1, id_equipo_local=1, id_equipo_visitante=2, equipo_local='Equipo1', equipo_visitante='Equipo2', fecha_partido='2020-10-10', resultado_local=10, resultado_visitante=20)
        Calendar.objects.create(num_jornada=1, id_game=2, id_equipo_local=4, id_equipo_visitante=3, equipo_local='Equipo4', equipo_visitante='Equipo3', fecha_partido='2020-10-10', resultado_local=10, resultado_visitante=20)
        Calendar.objects.create(num_jornada=2, id_game=3, id_equipo_local=2, id_equipo_visitante=1, equipo_local='Equipo2', equipo_visitante='Equipo1', fecha_partido='2020-10-11', resultado_local=10, resultado_visitante=20)
        Calendar.objects.create(num_jornada=2, id_game=4, id_equipo_local=3, id_equipo_visitante=4, equipo_local='Equipo3', equipo_visitante='Equipo4', fecha_partido='2020-10-11', resultado_local=10, resultado_visitante=20)

    def test_obtener_calendario(self):
        calendario = obtener_calendario(equipo=1, jornada=None)
        self.assertEqual(len(calendario), 2)
