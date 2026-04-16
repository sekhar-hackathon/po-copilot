import unittest
from dashboard import app

class DashboardTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Operator Dashboard', response.data)

    def test_health_scores_api(self):
        response = self.app.get('/api/health_scores')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('scores', data)
        self.assertIn('response_time', data)

if __name__ == '__main__':
    unittest.main()
