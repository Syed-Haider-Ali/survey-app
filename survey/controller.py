from .serializers import (SurveyFormSerializer, QuestionSerializer, QuestionOptionSerializer, QuestionTypeSerializer)
from utils.reusable_methods import get_first_error_message, paginate_data, get_params
from utils.response_messages import *
from utils.helper import create_response, paginate_data
from django.db import transaction
from .models import QuestionOption, Question
from .filters import SurveyFormFilter



class SurveyController:
    serializer_class = SurveyFormSerializer
    question_serializer = QuestionSerializer
    filterset_class = SurveyFormFilter
    def create(self, request):
        try:
            request.POST._mutable = True
            request.data['created_by'] = request.user.guid
            request.POST._mutable = False

            questions = request.data.pop("questions") if 'questions' in request.data else None
            if not questions:
                return create_response({}, 'Survey must contain questions', 400)
            elif len(questions) < 5:
                return create_response({}, "Add atleast 5 Questions", 400)
            elif len(questions) > 10:
                return create_response({}, "Allowed maximum 10 Questions", 400)

            serialized_data = self.serializer_class(data=request.data)
            if serialized_data.is_valid():
                with transaction.atomic():
                    response = serialized_data.save()

                    for que in questions:
                        options = que.pop("options") if 'options' in que else None
                        que['survey_form'] = response.id
                        serialized_question = QuestionSerializer(data=que)
                        if serialized_question.is_valid():
                            question = serialized_question.save()
                            if options:
                                options_list = [QuestionOption(option=o, question=question) for o in options]
                                QuestionOption.objects.bulk_create(options_list)
                        else:
                            transaction.set_rollback(True)
                            return create_response({}, get_first_error_message(serialized_question.errors,
                                                                               UNSUCCESSFUL), 400)

                return create_response(self.serializer_class(response).data, SUCCESSFUL, 200)
            else:
                return create_response({}, get_first_error_message(serialized_data.errors, UNSUCCESSFUL), 400)
        except Exception as e:
            return create_response({'error':str(e)}, UNSUCCESSFUL, 500)

    def list(self, request):
        try:
            instances = self.serializer_class.Meta.model.objects.all()

            filtered_data = self.filterset_class(request.GET, queryset=instances)
            data = filtered_data.qs

            paginated_data = paginate_data(data, request)
            count = data.count()

            serialized_data = self.serializer_class(paginated_data, many=True).data
            response_data = {
                "count": count,
                "data": serialized_data,
            }
            return create_response(response_data, SUCCESSFUL, 200)
        except Exception as e:
            return create_response({'error':str(e)}, UNSUCCESSFUL, 500)


    def destroy(self, request):
        try:
            if 'id' in request.query_params:
                kwargs = {}
                kwargs = get_params("id", request.query_params.get('id'), kwargs)
                instances = self.serializer_class.Meta.model.objects.filter(**kwargs)
                if instances:
                    for i in instances:
                        # questions = Question.objects.filter(survey_form=i.id)
                        questions = i.survey_questions.all()
                        for que in questions:
                            options = que.question_options.all()
                            if options:
                                options.delete()
                        questions.delete()
                    instances.delete()
                    return create_response({}, SUCCESSFUL, 200)
                else:
                    return create_response({}, NOT_FOUND, 404)
            else:
                return create_response({}, ID_NOT_PROVIDED, 400)
        except Exception as e:
            return create_response({'error':str(e)}, UNSUCCESSFUL, 500)


class QuestionTypeController:
    serializer_class = QuestionTypeSerializer
    def create(self, request):
        try:
            request.POST._mutable = True
            request.data['created_by'] = request.user.guid
            request.POST._mutable = False

            serialized_data = self.serializer_class(data=request.data)
            if serialized_data.is_valid():
                response = serialized_data.save()
                return create_response(self.serializer_class(response).data, SUCCESSFUL, 200)
            return create_response({}, get_first_error_message(serialized_data.errors, UNSUCCESSFUL),400)

        except Exception as e:
            return create_response({'error':str(e)}, UNSUCCESSFUL, 500)