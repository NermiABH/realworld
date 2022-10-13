import django_filters
from django_filters import filters, filterset
from .models import Article
from taggit.forms import TagField

class TagFilter(django_filters.CharFilter):
    field_class = TagField

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('lookup_expr', 'in')
        super().__init__(*args, **kwargs)


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class ArticleFilter(filterset.FilterSet):
    tags = TagFilter(field_name='tagList__name')
    author = CharFilterInFilter(field_name='author__username', lookup_expr='in')
    favorited = CharFilterInFilter(field_name='users_favourites__username', lookup_expr='in')
    class Meta:
        model = Article
        fields = ['tags', 'author', 'favorited']