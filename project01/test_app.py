from app import app
import unittest

class SearchViewTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_login_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/login')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_register_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/register')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_search_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/search')

        # assert the status code of the response
        self.assertEqual(result.status_code, 302)

if __name__ == "__main__":
    unittest.main()
