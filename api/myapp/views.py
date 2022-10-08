from rest_framework import viewsets, views
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Article, Comment, CustomUser
from .serializers import ArticleSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .services import ArticleFilter
from taggit.models import Tag
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # filter_backends = (DjangoFilterBackend,)
    # filterset_class = ArticleFilter
    lookup_field = 'slug'
    lookup_value_regex = '[?!feed]'
    default_fields_serializer = {}

    def get_serializer_context(self):
        return {'request': self.request}

    def list(self, request, *args, **kwargs):
        response_data = super().list(request, *args, **kwargs)
        response_data.data['articles'] = response_data.data.pop('results')
        response_data.data['articlesCount'] = self.queryset.count()
        return Response(response_data.data)

    @action(detail=False, methods=['GET'], url_path='feed', url_name='feed')
    def list_feed(self, request, *args, **kwargs):
        self.queryset = Article.objects.filter(author__in=request.user.sent_requests.all())
        return Response(self.list(request, *args, **kwargs).data)

    def retrieve(self, request, *args, **kwargs):
        response_data = super().retrieve(request, *args, **kwargs)
        return Response({'article': response_data.data})

    def create(self, request, *args, **kwargs):
        self.default_fields_serializer['author'] = request.user
        response_data = super().create(request, *args, **kwargs)
        return Response({'article': response_data.data})

    def perform_create(self, serializer):
        serializer.save(**self.default_fields_serializer)

    def update(self, request, *args, **kwargs):
        response_data = super().update(request, *args, **kwargs)
        return Response({'article': response_data.data})

    def change_field_M2M(self, request, queryset, manyfield, **kwargs):
        """New Function that add or remove a field for ManyToMany,
        such as like, dislike and favourite"""
        instance = queryset.get(**kwargs)
        if request.method == "POST":
            manyfield.add(instance)
        else:
            manyfield.remove(instance)
        request.method = 'GET'
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


    @action(detail=True, methods=['POST', 'DELETE'], url_path='favorite', lookup_field='slug')
    def favorite(self, request, *args, **kwargs):
        response_data = self.change_field_M2M(request, self.queryset, request.user.favourites, **kwargs)
        return Response(response_data.data)

    @action(detail=True, methods=['GET','POST'], url_path='comments',
            url_name='comments', serializer_class=CommentSerializer, queryset=Comment.objects.all())
    def comments(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(article__slug=kwargs.get('slug'))
        if request.method == 'POST':
            self.default_fields_serializer['author'] = request.user
            self.default_fields_serializer['article'] = Article.objects.get(slug=kwargs.get('slug'))
            response_data = super().create(request, *args, **kwargs)
            response_data.data = {'comment': response_data.data}
        else:
            response_data = super().list(request, *args, **kwargs)
            response_data.data['comments'] = response_data.data.pop('results')
        return Response(response_data.data)

    @action(detail=True, methods=['GET', 'PUT', 'DELETE'], url_path='comments/(?P<pk>[+]?\d+)',
            url_name='comments', serializer_class=CommentSerializer, queryset=Comment.objects.all(),
            lookup_field='pk')
    def comment(self, request, *args, **kwargs):
        if request.method == 'GET':
            response_data = super().retrieve(request, *args, **kwargs)
        elif request.method == 'PUT':
            instance = self.get_object()
            response_data = self.get_serializer(instance, data=request.data)
            response_data.is_valid(raise_exception=True)
            if not instance.changed:
                self.default_fields_serializer = {'changed':True}
            response_data.save(**self.default_fields_serializer)
        else:
            return Response(super().destroy(request, *args, **kwargs).data)
        return Response({'comment': response_data.data})

asdfffffffffffffffjalkgasldgfasljhg;jasng;asggsa
class TagList(views.APIView):
    def get(self, request):
        tags = Tag.objects.values_list('name', flat=True)
        return Response({'tags': tags})