from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth.models import User
from calendar_basket.models import Calendar, Teams
from perfil.models import Players

class ViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.team = Teams.objects.create(name="Equipo de prueba", id_team=1, id=1)
        self.player = Players.objects.create(user=self.user, id_team=self.team, first_name="Jugador de prueba")
        self.calendar = Calendar.objects.create(num_jornada=1, id_game=1, id_equipo_local=self.team.id_team,
                                                id_equipo_visitante=self.team.id_team, equipo_local="Local",
                                                equipo_visitante="Visitante", fecha_partido=timezone.now(),
                                                resultado_local=0, resultado_visitante=0)

    def test_view_statistics(self):
        client = Client()
        client.login(username='testuser', password='12345')

        response = client.get(reverse('statistics:statistics'))
        self.assertEqual(response.status_code, 200)

        response = client.get(reverse('statistics:statistics_game', kwargs={'id_game': self.calendar.id_game}))
        self.assertEqual(response.status_code, 200)

        response = client.get(reverse('statistics:statistics_game', kwargs={'id_game': 999}))
        self.assertEqual(response.status_code, 404)

        response = client.get(reverse('statistics:add_statistics', kwargs={'id_game': self.calendar.id_game}))
        self.assertEqual(response.status_code, 200)

        response = client.get(reverse('statistics:team_statistics'))
        self.assertEqual(response.status_code, 200)
