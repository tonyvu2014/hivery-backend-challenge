from app import app
import json
import unittest

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config.TestingConfig')
        self.app = app.test_client()

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status, '200 OK')

    def test_get_company_employees_404(self):
        response = self.app.get('/companies/100/employees')
        self.assertEqual(response.status, '404 NOT FOUND')

    def test_get_company_employees_empty_response(self):
        response = self.app.get('/companies/2/employees')
        self.assertEqual(response.status, '200 OK')
        data = json.loads(response.data)
        employees = data['employees']
        self.assertEqual(len(employees), 0)
    
    def test_get_company_employees_correct_response(self):
        response = self.app.get('/companies/1/employees')
        self.assertEqual(response.status, '200 OK')
        data = json.loads(response.data)
        employees = data['employees']
        self.assertEqual(len(employees), 2)
        self.assertEqual([1, 2], list(map(lambda x: x['index'], employees)))

    def test_get_filtered_common_friends_400(self):
        response = self.app.get('/people/filtered_common_friends?first_id=1&second_id=abc')
        self.assertEqual(response.status, '400 BAD REQUEST')

    def test_get_filtered_common_friends_404(self):
        response = self.app.get('/people/filtered_common_friends?first_id=4&second_id=2')
        self.assertEqual(response.status, '404 NOT FOUND')

    def test_get_filtered_common_friends_correct_response(self):
        response = self.app.get('/people/filtered_common_friends?first_id=0&second_id=3')
        self.assertEqual(response.status, '200 OK')
        data = json.loads(response.data)
        first_person = data['first_person']
        second_person = data['second_person']
        self.assertEqual(first_person['name'], 'Carmella Lambert')
        self.assertEqual(second_person['phone'], '+1 (984) 437-3226')
        filtered_common_friends = data['filtered_common_friends']
        self.assertEqual(len(filtered_common_friends), 1)
        self.assertEqual(filtered_common_friends[0]['index'], 1)

    def test_get_favourite_food_404(self):
        response = self.app.get('/people/5/favouriteFood')
        self.assertEqual(response.status, '404 NOT FOUND')
    
    def test_get_favourite_food_correct_response(self):
        response = self.app.get('/people/2/favouriteFood')
        data = json.loads(response.data)
        self.assertEqual(data['username'], 'Bonnie Bass')
        self.assertEqual(data['age'], 54)
        self.assertEqual(data['fruits'], ['orange', 'banana', 'strawberry'])
        self.assertEqual(data['vegetables'], ['beetroot'])

if __name__ == '__main__':
    unittest.main()