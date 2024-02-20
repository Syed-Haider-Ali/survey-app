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

    def test_create_survey_success(self):
        print('\n\ntest_create_survey_success')
        print('url:',self.url)
        payload = survey_payload('ideal')
        json_payload = json.dumps(payload)
        print('payload:',json_payload)
        response = self.client.post(self.url, json_payload, content_type='application/json')
        print('response:',response.json())
        assert response.status_code == status.HTTP_200_OK

    def test_create_survey_questions_lt_5(self):
        print('\ntest_create_survey_questions_lt_5')
        print('url:',self.url)
        payload = survey_payload('lt_5')
        json_payload = json.dumps(payload)
        print('payload:',json_payload)
        response = self.client.post(self.url, json_payload, content_type='application/json')
        print('response:',response.json())
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_survey_questions_gt_10(self):
        print('\ntest_create_survey_questions_gt_10')
        print('url:',self.url)
        payload = survey_payload('gt_10')
        json_payload = json.dumps(payload)
        print('payload:',json_payload)
        response = self.client.post(self.url, json_payload, content_type='application/json')
        print('response:',response.json())
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_survey_dropdown_questions_with_no_option(self):
        print('\ntest_create_survey_dropdown_questions_with_no_option')
        print('url:',self.url)
        payload = survey_payload('dropdown_questions_with_no_option')
        json_payload = json.dumps(payload)
        print('payload:',json_payload)
        response = self.client.post(self.url, json_payload, content_type='application/json')
        print('response:',response.json())
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
        print('\ntest_get_survey')
        print('url:',self.url)
        print('response:',response_data)
        assert response_data['data']['count'] == 1
        assert response.status_code == status.HTTP_200_OK

    def test_delete_survey_success(self):
        response = self.client.delete(self.url + f"?id={self.response_data['data']['id']}")
        print('\ntest_delete_survey_success')
        print('url:',self.url + f"?id={self.response_data['data']['id']}")
        print('response:', response.json())
        assert response.status_code == status.HTTP_200_OK

    def test_delete_survey_failed(self):
        response = self.client.delete(self.url + f"?id={111}")
        print('\ntest_delete_survey_failed')
        print('url:',self.url + f"?id={111}")
        print('response:', response.json())
        print('\n')
        assert response.status_code == status.HTTP_404_NOT_FOUND

