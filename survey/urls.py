from django.urls import path
from .views import SurveyView, QuestionTypeView, SubmitSurveyView, SurveyResultView

urlpatterns = [
    path('', SurveyView.as_view({'post': 'create', 'get': 'list', 'delete': 'destroy'})),

    path('question/type', QuestionTypeView.as_view({'post': 'create'})),

    path('submit/survey', SubmitSurveyView.as_view({'post': 'create'})),

    path('survey/results', SurveyResultView.as_view({'get': 'list'})),

]
