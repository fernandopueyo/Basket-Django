from django.test import TestCase

class ClasificacionViewsTestCase(TestCase):
    def test_clasificacion(self):
        response = self.client.get('/clasificacion/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clasificacion/clasificacion.html')