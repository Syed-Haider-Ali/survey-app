from django.db import models
from utils.reusable_classes import TimeStamps
from user_auth.models import User


class SurveyForm(TimeStamps):
    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

class Question(TimeStamps):
    survey_form = models.ForeignKey(SurveyForm, on_delete=models.CASCADE, related_name='survey_questions')
    type = models.ForeignKey('QuestionType', on_delete=models.CASCADE, related_name='question_types')
    body = models.TextField()

class QuestionType(TimeStamps):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

class QuestionOption(TimeStamps):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="question_options")
    option = models.CharField(max_length=500)

class SurveryFormQuestionAnswer(TimeStamps):
    survey_form = models.ForeignKey(SurveyForm, on_delete=models.DO_NOTHING, related_name='attempted_survey')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="attempted_question")
    chosen_answer = models.OneToOneField(QuestionOption, on_delete=models.CASCADE, null=True, blank=True,
                                         related_name="selected_option")
    descriptive_answer = models.TextField(null=True, blank=True)
    float_answer = models.FloatField(null=True, blank=True)
    answered_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='survey_answered_by')
