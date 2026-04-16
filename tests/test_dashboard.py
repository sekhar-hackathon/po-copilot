import unittest
from dashboard import app

class DashboardTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_dashboard_access(self):
        with self.client:
            # Simulate login
            self.client.post('/login', data=dict(username='operator', password='password'))
            response = self.client.get('/dashboard')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Operator Dashboard', response.data)

    def test_bearing_details_access(self):
        with self.client:
            # Simulate login
            self.client.post('/login', data=dict(username='operator', password='password'))
            response = self.client.get('/bearing/1')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Bearing Details', response.data)

if __name__ == '__main__':
    unittest.main()