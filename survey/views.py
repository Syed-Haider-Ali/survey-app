from .controller import SurveyController, QuestionTypeController
from rest_framework.viewsets import ModelViewSet
from utils.base_authentication import JWTAuthentication


survey_controller = SurveyController()
question_type_controller = QuestionTypeController()

class SurveyView(ModelViewSet):
    authentication_classes = (JWTAuthentication,)

    def create(self, request, *args, **kwargs):
        return survey_controller.create(request)

    def list(self, request, *args, **kwargs):
        return survey_controller.list(request)


class QuestionTypeView(ModelViewSet):
    authentication_classes = (JWTAuthentication,)

    def create(self, request, *args, **kwargs):
        return question_type_controller.create(request)
