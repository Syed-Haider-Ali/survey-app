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


class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['type'] = QuestionTypeSerializer(instance.type).data
        data['options'] = QuestionOptionSerializer(instance.question_options.all(), many=True).data if instance.question_options else None
        return data


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = '__all__'


class SurveryFormQuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveryFormQuestionAnswer
        fields = '__all__'


