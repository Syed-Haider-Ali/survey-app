from .controller import SurveyController, QuestionTypeController, SubmitSurveyController, SurveyResultController
from rest_framework.viewsets import ModelViewSet
from utils.base_authentication import JWTAuthentication


survey_controller = SurveyController()
question_type_controller = QuestionTypeController()
submit_survey_controller = SubmitSurveyController()
survey_result_controller = SurveyResultController()

class SurveyView(ModelViewSet):
    authentication_classes = (JWTAuthentication,)

    def create(self, request, *args, **kwargs):
        return survey_controller.create(request)

    def list(self, request, *args, **kwargs):
        return survey_controller.list(request)

    def destroy(self, request, *args, **kwargs):
        return survey_controller.destroy(request)

class QuestionTypeView(ModelViewSet):
    authentication_classes = (JWTAuthentication,)

    def create(self, request, *args, **kwargs):
        return question_type_controller.create(request)

class SubmitSurveyView(ModelViewSet):
    authentication_classes = (JWTAuthentication,)

    def create(self, request, *args, **kwargs):
        return submit_survey_controller.create(request)


class SurveyResultView(ModelViewSet):
    authentication_classes = (JWTAuthentication,)

    def list(self, request, *args, **kwargs):
        return survey_result_controller.list(request)


