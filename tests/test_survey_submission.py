import pytest
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user_auth.models import User
from survey.models import QuestionType
from .data import user_obj, survey_payload, submit_survey_form_payload


@pytest.mark.django_db
class TestSubmitSurvey:
    def setup_method(self):
        self.user = User.objects.create(**user_obj())
        arr = [QuestionType(title='descriptive', created_by=self.user),
               QuestionType(title='dropdown', created_by=self.user)]
        self.q_type = QuestionType.objects.bulk_create(arr)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.survey_url = reverse('survey_form')
        self.url = reverse('submit_survey')
        data = survey_payload('ideal')
        json_data = json.dumps(data)
        self.response = self.client.post(self.survey_url, json_data, content_type='application/json')
        self.response_data = self.response.json()

    def test_submit_survey_success(self):
        print('\n\ntest_submit_survey_success')
        print('url:',self.url)
        payload = submit_survey_form_payload(self.response_data['data']['id'])
        print('payload:',payload)
        response = self.client.post(self.url, payload, content_type='application/json')
        print('response:', response.json())
        assert response.status_code == status.HTTP_200_OK

    def test_submit_survey_failed_wrong_survey_id(self):
        print('\ntest_submit_survey_failed_wrong_survey_id')
        print('url:',self.url)
        payload = submit_survey_form_payload(111)
        print('payload:',payload)
        response = self.client.post(self.url, payload, content_type='application/json')
        print('response:', response.json())
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestListSurveyResponses:
    def setup_method(self):
        self.user = User.objects.create(**user_obj())
        arr = [QuestionType(title='descriptive', created_by=self.user),
               QuestionType(title='dropdown', created_by=self.user)]
        self.q_type = QuestionType.objects.bulk_create(arr)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        survey_url = reverse('survey_form')
        self.url = reverse('list_results')

        survey_payload_ = survey_payload('ideal')
        json_data = json.dumps(survey_payload_)
        self.response = self.client.post(survey_url, json_data, content_type='application/json')
        self.survey_response = self.response.json()
        submit_survey_payload = submit_survey_form_payload(self.survey_response['data']['id'])
        submit_survey_url = reverse('submit_survey')
        self.result = self.client.post(submit_survey_url, submit_survey_payload, content_type='application/json')

    def test_list_survey_response_success(self):
        print('\ntest_list_survey_response_success')
        print('url:',self.url + f"?id={self.survey_response['data']['id']}")
        response = self.client.get(self.url + f"?id={self.survey_response['data']['id']}")
        response_data = response.json()
        print('response:',response_data)
        print('\n')
        assert response_data['data']['total_responses'] == 1
        assert response.status_code == status.HTTP_200_OK

