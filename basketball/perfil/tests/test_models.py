from django.test import TestCase
from perfil.models import Players
from calendar_basket.models import Teams
from django.contrib.auth.models import User

class PlayersTestCase(TestCase):
    def setUp(self):
        Teams.objects.create(id_team=1, name='Equipo1', id=1)
        Teams.objects.create(id_team=2, name='Equipo2', id=2)
        User.objects.create(username='User1')
        User.objects.create(username='User2')
        Players.objects.create(id=1, user_id=1, id_team=Teams.objects.get(id_team=1), dorsal=1, first_name='Jugador1', last_name='Apellido1')
        Players.objects.create(id=2, user_id=2, id_team=Teams.objects.get(id_team=2), dorsal=2)

    def test_player(self):
        jugador1 = Players.objects.get(id=1)
        jugador2 = Players.objects.get(id=2)
        self.assertEqual(jugador1.first_name, 'Jugador1')
        self.assertEqual(jugador2.last_name, None)
        self.assertEqual(jugador1.id_team.id_team, 1)
        self.assertEqual(jugador2.dorsal, 2)
        self.assertEqual(jugador1.is_complete(), True)
        self.assertEqual(jugador2.is_complete(), False)