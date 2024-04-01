from django.test import TestCase
from statistics_basketball.models import Statistics, ShotStatistics, TeamStatistics
from calendar_basket.models import Calendar, Teams
from perfil.models import Players
from django.contrib.auth.models import User
from django.utils import timezone

class StatisticsBasketballModelTests(TestCase):
    def setUp(self):
        self.team = Teams.objects.create(name="Equipo de prueba", id_team=1, id=1)
        self.user = User.objects.create(username='User1')
        self.player = Players.objects.create(user=self.user, id_team=self.team, first_name="Jugador de prueba")
        self.calendar = Calendar.objects.create(num_jornada=1, id_game=1, id_equipo_local=self.team.id_team,
                                                 id_equipo_visitante=self.team.id_team, equipo_local="Local",
                                                 equipo_visitante="Visitante", fecha_partido=timezone.now(),
                                                 resultado_local=0, resultado_visitante=0)

    def test_statistics_model(self):
        stats = Statistics.objects.create(id_team=self.team, id_player=self.player, id_game=self.calendar,
                                           mins=30, fgm=10, fga=20, fgperc=0.5, threepm=5, threepa=10,
                                           threepperc=0.5, ftm=5, fta=5, ftperc=1, reb=5, ast=5, stl=2,
                                           blk=1, turnover=3, pf=4, pts=30, win=True)

        self.assertEqual(stats.id_team, self.team)
        self.assertEqual(stats.id_player, self.player)
        self.assertEqual(stats.id_game, self.calendar)
        self.assertEqual(stats.mins, 30)

    def test_shot_statistics_model(self):
        shot_stats = ShotStatistics.objects.create(id_team=self.team, id_player=self.player, id_game=self.calendar,
                                                    x=10, y=20, made=True, threep=True)

        self.assertEqual(shot_stats.id_team, self.team)
        self.assertEqual(shot_stats.id_player, self.player)
        self.assertEqual(shot_stats.id_game, self.calendar)
        self.assertEqual(shot_stats.x, 10)

    def test_team_statistics_model(self):
        team_stats = TeamStatistics.objects.create(id_team=self.team.id_team, team="Equipo de prueba",
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

        self.assertEqual(team_stats.id_team, self.team.id_team)
