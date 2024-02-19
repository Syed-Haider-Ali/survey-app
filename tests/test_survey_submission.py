import pytest
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user_auth.models import User
from django.contrib.auth.hashers import make_password
from survey.models import QuestionType


@pytest.mark.django_db
class TestSubmitSurvey:
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
        self.client.force_authenticate(user=self.user)

        self.survey_url = reverse('survey_form')
        self.url = reverse('submit_survey')

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
        self.response = self.client.post(self.survey_url, json_data, content_type='application/json')
        self.response_data = self.response.json()

    def test_submit_survey_success(self):
        payload = submit_survey_form_payload(self.response_data['data']['id'])
        response = self.client.post(self.url, payload, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK

    def test_submit_survey_failed_wrong_survey_id(self):
        payload = submit_survey_form_payload(111)
        response = self.client.post(self.url, payload, content_type='application/json')
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestListSurveyResponses:
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

        self.client.force_authenticate(user=self.user)

        survey_url = reverse('survey_form')
        self.url = reverse('list_results')

        survey_payload = {
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
        json_data = json.dumps(survey_payload)
        self.response = self.client.post(survey_url, json_data, content_type='application/json')
        self.survey_response = self.response.json()
        submit_survey_payload = submit_survey_form_payload(self.survey_response['data']['id'])
        submit_survey_url = reverse('submit_survey')
        self.result = self.client.post(submit_survey_url, submit_survey_payload, content_type='application/json')

    def test_list_survey_response_success(self):
        response = self.client.get(self.url + f"?id={self.survey_response['data']['id']}")
        response_data = response.json()
        assert response_data['data']['total_responses'] == 1
        assert response.status_code == status.HTTP_200_OK


def submit_survey_form_payload(survey_id):
        data = {
            "survey_form": survey_id,
            "answers": [
                {
                    "question": 1,
                    "descriptive_answer": "In about 30 mins"
                },
                {
                    "question": 2,
                    "descriptive_answer": "Obviously"
                },
                {
                    "question": 3,
                    "chosen_answer": 1
                },
                {
                    "question": 4,
                    "chosen_answer": 5
                },
                {
                    "question": 5,
                    "chosen_answer": 9
                },
                {
                    "question": 6,
                    "chosen_answer": 14
                }
            ]
        }
        json_data = json.dumps(data)

        return json_data

