from rest_framework import serializers
from user_auth.user_serializer import UserListingSerializer
from .models import *


class SurveyFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyForm
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['questions'] = QuestionSerializer(instance.survey_questions.all(), many=True).data
        data['created_by'] = UserListingSerializer(instance.created_by).data
        return data


class SurveyFormListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyForm
        fields = ['id', 'title']


class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = '__all__'


class QuestionTypeListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = ['id', 'title']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['type'] = QuestionTypeListingSerializer(instance.type).data
        data['options'] = QuestionOptionListingSerializer(instance.question_options.all(), many=True).data if instance.question_options else None
        return data


class QuestionListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['type'] = QuestionTypeListingSerializer(instance.type).data
        return data


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = '__all__'


class QuestionOptionListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ['id', 'option']


class SurveryFormQuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveryFormQuestionAnswer
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['survey_form'] = SurveyFormListingSerializer(instance.survey_form).data
        data['question'] = QuestionListingSerializer(instance.question).data
        data['chosen_answer'] = QuestionOptionListingSerializer(instance.chosen_answer).data if instance.chosen_answer else None
        data['answered_by'] = UserListingSerializer(instance.answered_by).data
        return data



