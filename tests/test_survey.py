import pytest
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user_auth.models import User
from django.contrib.auth.hashers import make_password
from survey.models import QuestionType


@pytest.mark.django_db
class TestCreateSurvey:
    def setup_method(self):
        user_data = {
            "first_name": "haider",
            "email": "haider@gmail.com",
            "username": "haider@gmail.com",
            "password": make_password("admin1234"),
            "is_active": True,
            "is_locked": False
        }
        self.user = User.objects.create(**user_data)
        arr = [QuestionType(title='descriptive', created_by=self.user), QuestionType(title='dropdown', created_by=self.user)]
        self. q_type = QuestionType.objects.bulk_create(arr)
        self.client = APIClient()
        self.url = reverse('survey_form')

    def test_survey_success(self):
        self.client.force_authenticate(user=self.user)
        data = {
    "title":"Pakistan Zindabad",
    "description":"Gathering Information Regarding Election 2024 Acceptance",
    "questions":[
        {
            "question":"How long will you take to do this?",
            "type":1
        },
        {
            "question":"Will you accept Mian sb?",
            "type":1
        },
        {
            "question":"How long will you take to do this",
            "type":2,
            "options":["first one", "second one", "third one", "fourth one"]
        },
        {
            "question":"How long will you take to do this",
            "type":2,
            "options":["fifth one", "sixth one", "seventh one", "eighteth one"]
        },
        {
            "question":"How long will you take to do this",
            "type":2,
            "options":["ninth one", "Tenth one", "Eleventh one", "Twelth one"]
        },
        {
            "question":"How long will you take to do this",
            "type":2,
            "options":["Thirteenth one", "Fourteenth one", "Fifteenth one", "Sixteenth one"]
        }
    ]
}
        json_data = json.dumps(data)
        response = self.client.post(self.url, json_data, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK

    def test_survey_questions_lt_5(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "Pakistan Zindabad",
            "description": "Gathering Information Regarding Election 2024 Acceptance",
            "questions": [
                {
                    "question": "How long will you take to do this?",
                    "type": 1
                },
                {
                    "question": "Will you accept Mian sb?",
                    "type": 1
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["first one", "second one", "third one", "fourth one"]
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["fifth one", "sixth one", "seventh one", "eighteth one"]
                },
            ]
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, json_data, content_type='application/json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_survey_questions_gt_10(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "Pakistan Zindabad",
            "description": "Gathering Information Regarding Election 2024 Acceptance",
            "questions": [
                {
                    "question": "How long will you take to do this?",
                    "type": 1
                },
                {
                    "question": "Will you accept Mian sb?",
                    "type": 1
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["first one", "second one", "third one", "fourth one"]
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["fifth one", "sixth one", "seventh one", "eighteth one"]
                },
                {
                    "question": "How long will you take to do this?",
                    "type": 1
                },
                {
                    "question": "Will you accept Mian sb?",
                    "type": 1
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["first one", "second one", "third one", "fourth one"]
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["fifth one", "sixth one", "seventh one", "eighteth one"]
                },
                {
                    "question": "How long will you take to do this?",
                    "type": 1
                },
                {
                    "question": "Will you accept Mian sb?",
                    "type": 1
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["first one", "second one", "third one", "fourth one"]
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["fifth one", "sixth one", "seventh one", "eighteth one"]
                },
            ]
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, json_data, content_type='application/json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_survey_dropdown_questions_with_no_option(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "Pakistan Zindabad",
            "description": "Gathering Information Regarding Election 2024 Acceptance",
            "questions": [
                {
                    "question": "How long will you take to do this?",
                    "type": 2
                },
                {
                    "question": "Will you accept Mian sb?",
                    "type": 2
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["first one", "second one", "third one", "fourth one"]
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["fifth one", "sixth one", "seventh one", "eighteth one"]
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["ninth one", "Tenth one", "Eleventh one", "Twelth one"]
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["Thirteenth one", "Fourteenth one", "Fifteenth one", "Sixteenth one"]
                }
            ]
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, json_data, content_type='application/json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestListDeleteSurvey:

    def setup_method(self):
        user_data = {
            "first_name": "haider",
            "email": "haider@gmail.com",
            "username": "haider@gmail.com",
            "password": make_password("admin1234"),
            "is_active": True,
            "is_locked": False
        }
        self.user = User.objects.create(**user_data)

        arr = [QuestionType(title='descriptive', created_by=self.user),
               QuestionType(title='dropdown', created_by=self.user)]
        self.q_type = QuestionType.objects.bulk_create(arr)

        self.client = APIClient()
        self.url = reverse('survey_form')
        self.client.force_authenticate(user=self.user)

        data = {
            "title": "Pakistan Zindabad",
            "description": "Gathering Information Regarding Election 2024 Acceptance",
            "questions": [
                {
                    "question": "How long will you take to do this?",
                    "type": 1
                },
                {
                    "question": "Will you accept Mian sb?",
                    "type": 1
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["first one", "second one", "third one", "fourth one"]
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["fifth one", "sixth one", "seventh one", "eighteth one"]
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["ninth one", "Tenth one", "Eleventh one", "Twelth one"]
                },
                {
                    "question": "How long will you take to do this",
                    "type": 2,
                    "options": ["Thirteenth one", "Fourteenth one", "Fifteenth one", "Sixteenth one"]
                }
            ]
        }
        json_data = json.dumps(data)
        self.response = self.client.post(self.url, json_data, content_type='application/json')
        self.response_data = self.response.json()

    def test_get_survey(self):
        response = self.client.get(self.url)
        response_data = response.json()
        assert response_data['data']['count'] == 1
        assert response.status_code == status.HTTP_200_OK

    def test_delete_survey_success(self):
        response = self.client.delete(self.url + f"?id={self.response_data['data']['id']}")
        assert response.status_code == status.HTTP_200_OK

    def test_delete_survey_failed(self):
        response = self.client.delete(self.url + f"?id={111}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

