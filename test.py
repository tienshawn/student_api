import unittest
from unittest.mock import patch, MagicMock
from flask import json
from app import application
from bson import ObjectId



class FlaskAppTestCase(unittest.TestCase):
    # MONGO_student_database_URI = "mongodb://"
    # TESTING = True

    def setUp(self):
        self.client = application.test_client()
        self.client.testing = True

        # student_database.create_all()
        # application.config["TESTING"] = True


    def tearDown(self):
        pass

        # student_database.session.remove()
        # student_database.drop_all()

    @patch('app.student_database')
    def test_get_all(self, mock_student_database):
        mock_student_database.find.return_value = [
                {
                    '_id': '1',
                    'name': 'Name_1',
                    'gender': 'Gender_1',
                    'birth': 'Birth_1',
                    'university': 'University_1',
                    'country': 'Country_1'
                },
                {
                   '_id': '2',
                    'name': 'Name_2',
                    'gender': 'Gender_2',
                    'birth': 'Birth_2',
                    'university': 'University_2',
                    'country': 'Country_2' 
                }
            ]

        response_get = self.client.get("/")
        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(len(response_get.json), 2)
        self.assertEqual(response_get.json[0]['name'], 'Name_1')
        self.assertEqual(response_get.json[1]['name'], 'Name_2')

    @patch('app.student_database')
    def test_create_student(self, mock_student_database):
        mock_student_database.insert_one.return_value = [
            {
                'name': 'Test Name',
                'birth': '2003',
                'gender': 'Test Gender',
                'university': 'Test University',
                'country': 'Test Country'
            }
        ]

        response_create = self.client.get("/", method = 'POST')
        self.assertEqual(response_create.status_code, 200)

    @patch('app.student_database')
    def test_get_student(self, mock_student_database):
        student_id =  '60b8d295f1d4f2bde4148b9a'
        mock_student_database.find_one.return_value = {
                '_id': ObjectId(student_id),
                'name': 'Test_Name',
                'gender': 'Test_Gender',
                'university': 'Test_University',
                'birth': '2003',
                'country': 'Test_Country'
            }
        
        response_get = self.client.get(f'/{student_id}')
        self.assertEqual(response_get.status_code, 200)


    @patch('app.student_database')
    def test_delete(self, mock_student_database):
        mock_student_database.delete_one.return_value = 0

        student_id = ObjectId('60b8d295f1d4f2bde4148b9a')
        response_get = self.client.delete(f'/{student_id}')
        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(response_get.json['status'], 'success')

    @patch('app.student_database')
    def test_update(self, mock_student_database):
        student_id = ObjectId('60b8d295f1d4f2bde4148b9a')
        mock_student_database.find_one.return_value = {
                '_id': ObjectId(student_id),
                'name': 'Test_Name',
                'gender': 'Test_Gender',
                'university': 'Test_University',
                'birth': '2003',
                'country': 'Test_Country'
            }
        mock_student_database.update_one.return_value = MagicMock(matched_count=1, modified_count=1)

        updated_data = {
            'name': 'Update_Name',
            'gender': 'Test_Gender',
            'university': 'Test_University',
            'birth': '2003',
            'country': 'Test_Country'
        }
        
        # Perform the PUT request
        response_update = self.client.put(f'/{student_id}', data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(response_update.status_code, 200)
        self.assertEqual(response_update.json['status'], 'success')


        
if __name__ == '__main__':
    unittest.main()



