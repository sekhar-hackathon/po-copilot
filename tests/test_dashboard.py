import unittest
from dashboard import app

class DashboardTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_dashboard_view(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard for Plant A', response.data)

    def test_details_view(self):
        response = self.app.get('/details/Plant A/Bearing 1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Details for Bearing 1 in Plant A', response.data)

if __name__ == '__main__':
    unittest.main()