import django_filters
from django_filters import DateFilter, CharFilter

from .models import *


class SLotFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_happened", lookup_expr='gte')
    end_date = DateFilter(field_name="date_happened", lookup_expr='lte')


    class Meta:
        model = Slot
        fields = '__all__'
        exclude = ['customer', 'date_happened']

