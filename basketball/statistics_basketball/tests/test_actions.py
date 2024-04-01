from django.test import TestCase, Client, RequestFactory
from django.http import Http404
from django.utils import timezone

from statistics_basketball.models import Statistics, ShotStatistics, TeamStatistics
from calendar_basket.models import Calendar, Teams
from perfil.models import Players
from django.contrib.auth.models import User

from statistics_basketball.actions import player_login, obtener_partido

class StatisticsActionsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.team = Teams.objects.create(name="Equipo de prueba", id_team=1, id=1)
        self.player = Players.objects.create(user=self.user, id_team=self.team, first_name="Jugador de prueba")
        self.calendar = Calendar.objects.create(num_jornada=1, id_game=1, id_equipo_local=self.team.id_team,
                                                id_equipo_visitante=self.team.id_team, equipo_local="Local",
                                                equipo_visitante="Visitante", fecha_partido=timezone.now(),
                                                resultado_local=0, resultado_visitante=0)
        self.statistics = Statistics.objects.create(id_team=self.team, id_player=self.player, id_game=self.calendar,
                                                    mins=30, fgm=10, fga=20, fgperc=0.5, threepm=5, threepa=10,
                                                    threepperc=0.5, ftm=5, fta=5, ftperc=1, reb=5, ast=5, stl=2,
                                                    blk=1, turnover=3, pf=4, pts=30, win=True)
        self.shot_stats = ShotStatistics.objects.create(id_team=self.team, id_player=self.player, id_game=self.calendar,
                                                        x=10, y=20, made=True, threep=True)
        self.team_stats = TeamStatistics.objects.create(id_team=self.team.id_team, team="Equipo de prueba",
                                                        posicion=1, jugados=1, ganados=1, perdidos=0,
                                                        puntos_favor=100.0, puntos_contra=80.0, dif_puntos=20.0,
                                                        g_puntos_favor=25.0, g_puntos_contra=20.0, g_dif_puntos=5.0,
                                                        p_puntos_favor=75.0, p_puntos_contra=60.0, p_dif_puntos=15.0,
                                                        c_posicion=1, c_jugados=1, c_ganados=1, c_perdidos=0,
                                                        c_puntos_favor=100.0, c_puntos_contra=80.0, c_dif_puntos=20.0,
                                                        c_g_puntos_favor=25.0, c_g_puntos_contra=20.0,
                                                        c_g_dif_puntos=5.0, c_p_puntos_favor=75.0,
                                                        c_p_puntos_contra=60.0, c_p_dif_puntos=15.0,
                                                        f_posicion=1, f_jugados=1, f_ganados=1, f_perdidos=0,
                                                        f_puntos_favor=100.0, f_puntos_contra=80.0, f_dif_puntos=20.0,
                                                        f_g_puntos_favor=25.0, f_g_puntos_contra=20.0,
                                                        f_g_dif_puntos=5.0, f_p_puntos_favor=75.0,
                                                        f_p_puntos_contra=60.0, f_p_dif_puntos=15.0)
        self.factory = RequestFactory()

    def test_player_login_existing_player(self):
        request = self.factory.get('/')
        request.user = self.user
        logged_player = player_login(request)

        self.assertEqual(logged_player, self.player)
    
    def test_player_login_no_player(self):
        request = self.factory.get('/')
        request.user = User.objects.create_user(username='testuser2', password='12345')
        logged_player = player_login(request)

        self.assertEqual(logged_player, None)

    def test_player_login_no_user(self):
        request = self.factory.get('/')
        request.user = None
        logged_player = player_login(request)

        self.assertEqual(logged_player, None)

    def test_obtener_partido_game(self):
        id_game = self.calendar.id_game
        game = obtener_partido(id_game)
        self.assertEqual(game, self.calendar)

    def test_obtener_partido_no_game(self):
        with self.assertRaises(Http404):
            obtener_partido(id_game=999)