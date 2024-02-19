import pytest
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user_auth.models import User
from django.contrib.auth.hashers import make_password
from survey.models import QuestionType
from .data import survey_payload, user_obj


@pytest.mark.django_db
class TestCreateSurvey:
    def setup_method(self):

        self.client = APIClient()
        self.user = User.objects.create(**user_obj())
        self.client.force_authenticate(user=self.user)
        arr = [QuestionType(title='descriptive', created_by=self.user), QuestionType(title='dropdown', created_by=self.user)]
        self. q_type = QuestionType.objects.bulk_create(arr)
        self.url = reverse('survey_form')

    def test_survey_success(self):
        data = survey_payload('ideal')
        json_data = json.dumps(data)
        response = self.client.post(self.url, json_data, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK

    def test_survey_questions_lt_5(self):
        data = survey_payload('lt_5')
        json_data = json.dumps(data)
        response = self.client.post(self.url, json_data, content_type='application/json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_survey_questions_gt_10(self):
        data = survey_payload('gt_10')
        json_data = json.dumps(data)
        response = self.client.post(self.url, json_data, content_type='application/json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_survey_dropdown_questions_with_no_option(self):
        data = survey_payload('dropdown_questions_with_no_option')
        json_data = json.dumps(data)
        response = self.client.post(self.url, json_data, content_type='application/json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestListDeleteSurvey:

    def setup_method(self):

        self.user = User.objects.create(**user_obj())
        arr = [QuestionType(title='descriptive', created_by=self.user),
               QuestionType(title='dropdown', created_by=self.user)]
        self.q_type = QuestionType.objects.bulk_create(arr)

        self.client = APIClient()
        self.url = reverse('survey_form')
        self.client.force_authenticate(user=self.user)

        data = survey_payload('ideal')
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

