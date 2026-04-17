import unittest
from dashboard import app

class DashboardTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_dashboard_loads(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Operator Dashboard', response.data)

    def test_health_scores_display(self):
        response = self.app.get('/')
        self.assertIn(b'Plant A', response.data)
        self.assertIn(b'Bearing 1', response.data)
        self.assertIn(b'85', response.data)

if __name__ == '__main__':
    unittest.main()