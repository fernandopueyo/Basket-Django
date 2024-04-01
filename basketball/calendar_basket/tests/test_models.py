from django.test import TestCase
from calendar_basket.models import Calendar, Teams

class CalendarTestCase(TestCase):
    def setUp(self):
        Calendar.objects.create(num_jornada=1, id_game=1, id_equipo_local=1, id_equipo_visitante=2, equipo_local='Equipo1', equipo_visitante='Equipo2', fecha_partido='2020-10-10', resultado_local=1, resultado_visitante=2)
        Calendar.objects.create(num_jornada=2, id_game=2, id_equipo_local=3, id_equipo_visitante=4, equipo_local='Equipo3', equipo_visitante='Equipo4', fecha_partido='2020-10-11', resultado_local=3, resultado_visitante=4)

    def test_calendar(self):
        """Calendar are correctly identified"""
        calendar1 = Calendar.objects.get(num_jornada=1)
        calendar2 = Calendar.objects.get(num_jornada=2)
        self.assertEqual(calendar1.equipo_local, 'Equipo1')
        self.assertEqual(calendar2.equipo_local, 'Equipo3')

class TeamsTestCase(TestCase):
    def setUp(self):
        Teams.objects.create(id=1, name='Equipo1', id_team=1)
        Teams.objects.create(id=2, name='Equipo2', id_team=2)

    def test_teams(self):
        """Teams are correctly identified"""
        team1 = Teams.objects.get(id=1)
        team2 = Teams.objects.get(id=2)
        self.assertEqual(team1.name, 'Equipo1')
        self.assertEqual(team2.name, 'Equipo2')

