import unittest
from dashboard import app

class DashboardTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_dashboard_loads(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bearing Health Dashboard', response.data)

if __name__ == '__main__':
    unittest.main()