from django_filters import DateFilter, CharFilter, FilterSet
from .models import SurveyForm

class SurveyFormFilter(FilterSet):
    id = CharFilter(field_name='id')
    date_from = DateFilter(field_name='created_at', lookup_expr='gte' )
    date_to = DateFilter(field_name='created_at', lookup_expr='lte' )
    date = DateFilter(field_name='created_at__date')
    title = CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = SurveyForm
        fields ='__all__'