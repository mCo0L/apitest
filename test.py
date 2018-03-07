import unittest
import os
from script import app
#from Api import app

class ApiTestCase(unittest.TestCase):
    url = 'http://127.0.0.1:8000/'
    def setUp(self):
        self.app = app
        self.app.testing = True
        self.client = self.app.test_client()

    def test_post_location(self):
        print('\ncurrent test: ' + self._testMethodName)
        data = "99.951+76.264+IN/121072+Pipli+Haryana"
        result = self.client.post(self.url+"post_location",data=data, content_type='text/plain')
        self.assertEqual(result.status_code, 200)
        print('/post_location : result - '+str(result.data))

    def test_get_using_postgres(self):
        print('\ncurrent test: ' + self._testMethodName)
        data = "28.609+77.223"
        result = self.client.get(self.url+"get_using_postgres",data=data, content_type='text/plain')
        self.assertEqual(result.status_code, 200)
        print('/get_using_postgres : result - '+str(result.data))


    def test_get_using_self(self):
        print('\ncurrent test: ' + self._testMethodName)
        data = "28.609+77.223"
        result = self.client.get(self.url+"get_using_self",data=data, content_type='text/plain')
        self.assertEqual(result.status_code, 200)
        print('/get_using_self : result - '+str(result.data))


    def test_api_get_location(self):
        print('\ncurrent test: ' + self._testMethodName)
        data = "28.609+77.223"
        result = self.client.get(self.url+"get_city_name",data=data, content_type='text/plain')
        self.assertEqual(result.status_code, 200)
        print('/get_using_self : result - '+str(result.data))

    def tearDown(self):
        pass
if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
