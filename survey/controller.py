from .serializers import (SurveyFormSerializer, QuestionSerializer, QuestionOptionSerializer, QuestionTypeSerializer)
from utils.reusable_methods import get_first_error_message
from utils.response_messages import *
from utils.helper import create_response, paginate_data
from django.db import transaction
from .models import QuestionOption, Question

class SurveyController:
    serializer_class = SurveyFormSerializer
    question_serializer = QuestionSerializer
    def create(self, request):
        try:
            request.POST._mutable = True
            request.data['created_by'] = request.user.guid
            request.POST._mutable = False

            questions = request.data.pop("questions") if request.data['questions'] else None

            serialized_data = self.serializer_class(data=request.data)
            if serialized_data.is_valid():
                with transaction.atomic():
                    response = serialized_data.save()

                    if questions:
                        if len(questions) < 5:
                            transaction.set_rollback(True)
                            return create_response({}, "Survey should contain atleast 5 Questions", 400)
                        elif len(questions) > 10:
                            transaction.set_rollback(True)
                            return create_response({}, "Survey should contains maximum 10 Questions", 400)

                        questions_list = []
                        for i in questions:
                            options = request.data.pop("options") if i['options'] else None
                            #if options then create question in single query
                            if options:
                                serialized_question = QuestionSerializer(data=i)
                                if serialized_question.is_valid():
                                    question = serialized_question.save()
                                    options_list = [QuestionOption(title=o, question=question) for o in options]
                                    QuestionOption.objects.bulk_create(options_list)
                                else:
                                    transaction.set_rollback(True)
                                    return create_response({}, get_first_error_message(serialized_question.errors,
                                                                                       UNSUCCESSFUL), 400)
                            #if question is descriptive create in bulk create to reduce query.
                            else:
                                questions_list.append(Question(question))

                            serialized_question = QuestionSerializer(data=i)
                            if serialized_question.is_valid():
                                question = serialized_question.save()
                                if options:
                                   options_list = [QuestionOption(title=o, question=question) for o in options]
                                   QuestionOption.objects.bulk_create(options_list)
                            else:
                                transaction.set_rollback(True)
                                return create_response({}, get_first_error_message(serialized_question.errors, UNSUCCESSFUL), 400)



                return create_response(response, SUCCESSFUL, 200)
            return create_response({}, get_first_error_message(serialized_data.errors, UNSUCCESSFUL), 400)
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
                return create_response(response, SUCCESSFUL, 200)
            return create_response({}, get_first_error_message(serialized_data.errors, UNSUCCESSFUL),400)

        except Exception as e:
            return create_response({'error':str(e)}, UNSUCCESSFUL, 500)