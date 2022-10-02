from rest_framework import viewsets
from .models import Article
from .serializers import ArticleSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .services import ArticleFilter
from rest_framework.response import Response


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ArticleFilter
    lookup_field = 'slug'

    def get_serializer_context(self):
        return {'request': self.request}

    def list_feed(self, request, *args, **kwargs):
        response_data = super().list(request, *args, **kwargs)
        return Response(response_data.data)

    def retrieve(self, request, *args, **kwargs):
        response_data = super().retrieve(request, *args, **kwargs)
        return Response({
            'article': response_data.data
        })

