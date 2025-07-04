import django_filters
from django_filters import FilterSet

from .models import Snippet


class SnippetFilter(FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    language = django_filters.NumberFilter(field_name="language__id")
    tags = django_filters.NumberFilter(field_name="tags__id")
    categories = django_filters.NumberFilter(field_name="categories__id")

    class Meta:
        model = Snippet
        fields = ['name', 'language', 'tags', 'categories']
