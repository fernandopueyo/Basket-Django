from django.test import TestCase

class CalendarViewTestCase(TestCase):
    def test_calendar_view(self):
        response = self.client.get('/calendar/')
        self.assertEqual(response.status_code, 200)
