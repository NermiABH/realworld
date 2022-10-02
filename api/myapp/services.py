from django_filters import rest_framework as filters
from .models import Article
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ArticleFilter(filters.FilterSet):
    title = CharFilterInFilter(field_name='title__name', lookup_expr='in')

    class Meta:
        model = Article
        fields = ['title']


class CustomLimitOffsetPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response({
            'count_pages': self.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'articles': data,
            'articleCount': len(data),
        })
