from django.urls import path
from .views import SurveyView, QuestionTypeView

urlpatterns = [
    path('', SurveyView.as_view({'post':'create', 'get':'list'})),
    path('question/type', QuestionTypeView.as_view({'post': 'create'})),
]
