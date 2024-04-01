from django.test import TestCase
from calendar_basket.models import Teams
from clasificacion.models import Clasificacion

class ClasificacionTestCase(TestCase):
    def setUp(self):
        Teams.objects.create(id_team=1, name='Equipo1', id=1)
        Teams.objects.create(id_team=2, name='Equipo2', id=2)
        Teams.objects.create(id_team=3, name='Equipo3', id=3)
        Teams.objects.create(id_team=4, name='Equipo4', id=4)
        Clasificacion.objects.create(id_team=Teams.objects.get(id_team=1), posicion=1, jugados=1, puntos=3, ganados=1, perdidos=0, puntos_favor=10, puntos_contra=5, racha='2')
        Clasificacion.objects.create(id_team=Teams.objects.get(id_team=2), posicion=2, jugados=1, puntos=0, ganados=0, perdidos=1, puntos_favor=5, puntos_contra=10, racha='-2')
        Clasificacion.objects.create(id_team=Teams.objects.get(id_team=3), posicion=3, jugados=1, puntos=3, ganados=1, perdidos=0, puntos_favor=10, puntos_contra=5, racha='2')
        Clasificacion.objects.create(id_team=Teams.objects.get(id_team=4), posicion=4, jugados=1, puntos=0, ganados=0, perdidos=1, puntos_favor=5, puntos_contra=10, racha='-2')
        

    def test_nombre_equipo(self):
        equipo1 = Clasificacion.objects.get(id_team=1)
        equipo2 = Clasificacion.objects.get(id_team=2)
        equipo3 = Clasificacion.objects.get(id_team=3)
        equipo4 = Clasificacion.objects.get(id_team=4)
        self.assertEqual(equipo1.posicion, 1)
        self.assertEqual(equipo2.jugados, 1)
        self.assertEqual(equipo3.puntos_favor, 10)
        self.assertEqual(equipo4.racha, '-2')