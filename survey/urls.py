from django.urls import path
from .views import SurveyView, QuestionTypeView, SubmitSurveyView, SurveyResultView

urlpatterns = [
    path('', SurveyView.as_view({'post': 'create', 'get': 'list', 'delete': 'destroy'}), name='survey_form'),
    path('question/type', QuestionTypeView.as_view({'post': 'create', 'get': 'list'})),
    path('submit/survey', SubmitSurveyView.as_view({'post': 'create'}), name='submit_survey'),
    path('survey/results', SurveyResultView.as_view({'get': 'list'}), name='list_results'),
]
