from django_filters import FilterSet, AllValuesFilter
from django_filters import NumberFilter


class ProductFilter(FilterSet):
    min_price = NumberFilter(field_name='regular_price' , lookup_expr='gte')
    max_price = NumberFilter(field_name='regular_price' , lookup_expr='lte')