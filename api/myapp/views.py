from rest_framework import viewsets
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSerializer
# from .services import ArticleFilter


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # filter_backends = ArticleFilter
    lookup_field = 'slug'

    def get_serializer_context(self):
        return {'request': self.request}

    def list(self, request, *args, **kwargs):
        response_data = super().list(request, *args, **kwargs)
        response_data.data['articlesCount'] = self.queryset.count()
        return Response(response_data.data)

    def list_feed(self, request, *args, **kwargs):
        response_data = super().list(request, *args, **kwargs)
        response_data.data['articlesCount'] = self.queryset.count()
        return Response(response_data.data)

    def retrieve(self, request, *args, **kwargs):
        response_data = super().retrieve(request, *args, **kwargs)
        return Response({
            'article': response_data.data
        })
