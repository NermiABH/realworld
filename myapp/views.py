from rest_framework import viewsets, views, pagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from taggit.models import Tag
from django_filters.rest_framework import DjangoFilterBackend
from .models import Article, Comment, CustomUser
from .serializers import ArticleSerializer, CommentSerializer, UserSerializer
from .services import ArticleFilter
from djoser.views import UserViewSet
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth.views import auth_logout


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


def exception_handler(exc, context):
    response = views.exception_handler(exc, context)
    if response.status_code == 400:
        response.data = {
            'errors': response.data
        }
    elif response.status_code == 404:
        response.data['errors'] = {
            'obj': response.data.pop('detail')
        }
    elif response.status_code == 405:
        response.data['errors'] = {
            'method': response.data.pop('detail')
        }
    elif response.status_code == 401:
        response.data['errors'] = {
            'permission': response.data.pop('detail')
        }
    return Response(response.data, status=response.status_code, headers=response.headers)


class UserCustomViewSet(UserViewSet):
    pagination_class = None
    def get_serializer_context(self):
        return {'request': self.request,
                'kwargs': self.kwargs}

    @action(methods=['POST', 'DELETE'],detail=False)
    def follow_profile(self, request, *args, **kwargs):
        self.queryset = CustomUser.objects.get(kwargs.get('username'))
        response_data = change_field_M2M(request, self.queryset, request.user.sent_requests, **kwargs)
        return Response(response_data.data)

class ArticleCommentViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ArticleFilter
    lookup_field = 'slug'
    default_fields_serializer = {}
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_serializer_context(self):
        return {'request': self.request}

    def list(self, request, *args, **kwargs):
        response_data = super().list(request, *args, **kwargs)
        response_data.data['articles'] = response_data.data.pop('results')
        response_data.data['articlesCount'] = self.queryset.count()
        return Response(response_data.data)

    @action(detail=False, methods=['GET'], url_path='feed', url_name='feed', permission_classes=(IsAuthenticated,))
    def list_feed(self, request, *args, **kwargs):
        self.queryset = Article.objects.filter(author__in=request.user.sent_requests.all())
        return Response(self.list(request, *args, **kwargs).data)

    def retrieve(self, request, *args, **kwargs):
        response_data = super().retrieve(request, *args, **kwargs)
        return Response({'article': response_data.data})

    def create(self, request, *args, **kwargs):
        self.default_fields_serializer['author'] = request.user
        response_data = super().create(request, *args, **kwargs)
        return Response({'article': response_data.data},
                        status=response_data.status_code,
                        headers=response_data.headers)

    def perform_create(self, serializer):
        serializer.save(**self.default_fields_serializer)

    def update(self, request, *args, **kwargs):
        response_data = super().update(request, *args, **kwargs)
        return Response({'article': response_data.data},
                        status=response_data.status_code,
                        headers=response_data.headers)

    @action(detail=True, methods=['POST', 'DELETE'], url_path='favorited',
            lookup_field='slug', permission_classes=(IsAuthenticated,))
    def favorite(self, request, *args, **kwargs):
        response_data = change_field_M2M(request, self.queryset, request.user.favourites, **kwargs)
        return Response(response_data.data, status=response_data.status_code, headers=response_data.headers)

    @action(detail=True, methods=['POST', 'DELETE'], url_path='liked',
            lookup_field='slug', permission_classes=(IsAuthenticated,))
    def like_article(self, request, *args, **kwargs):
        response_data = change_field_M2M(request, self.queryset, request.user.liked_articles, **kwargs)
        return Response(response_data.data, status=response_data.status_code, headers=response_data.headers)

    @action(detail=True, methods=['POST', 'DELETE'], url_path='disliked',
            lookup_field='slug', permission_classes=(IsAuthenticated,))
    def dislike_article(self, request, *args, **kwargs):
        response_data = change_field_M2M(request, self.queryset, request.user.disliked_articles, **kwargs)
        return Response(response_data.data, status=response_data.status_code, headers=response_data.headers)

    @action(detail=True, methods=['GET','POST'], url_path='comments',
            url_name='comments', serializer_class=CommentSerializer,
            queryset=Comment.objects.all(), permission_classes=(IsAuthenticatedOrReadOnly,))
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
        return Response(response_data.data, status=response_data.status_code, headers=response_data.headers)

    @action(detail=True, methods=['GET', 'PUT', 'DELETE'], url_path='comments/(?P<pk>[+]?\d+)',
            url_name='comments', serializer_class=CommentSerializer, queryset=Comment.objects.all(),
            lookup_field='pk', permission_classes = (IsAuthenticatedOrReadOnly,))
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
            response_data = super().destroy(request, *args, **kwargs)
            return Response(response_data.data, status=response_data.status_code)
        return Response({'comment': response_data.data},
                        status=response_data.status_code,
                        headers=response_data.headers)

    @action(detail=True, methods=['POST', 'DELETE'], url_path='comments/(?P<pk>[+]?\d+)/liked',
            lookup_field='pk', queryset = Comment.objects.all(), serializer_class=CommentSerializer,
            permission_classes = (IsAuthenticated,))
    def like_comment(self, request, *args, **kwargs):
        kwargs.pop('slug')
        response_data = change_field_M2M(request, self.queryset, request.user.liked_comments, **kwargs)
        return Response(response_data.data, status=response_data.status_code, headers=response_data.headers)

    @action(detail=True, methods=['POST', 'DELETE'], url_path='comments/(?P<pk>[+]?\d+)/disliked',
            lookup_field='pk', queryset = Comment.objects.all(), serializer_class=CommentSerializer,
            permission_classes = (IsAuthenticated,))
    def dislike_comment(self, request, *args, **kwargs):
        kwargs.pop('slug')
        response_data = change_field_M2M(request, self.queryset, request.user.disliked_comments, **kwargs)
        return Response(response_data.data, status=response_data.status_code, headers=response_data.headers)


class TagList(views.APIView):
    def get(self, request):
        tags = Tag.objects.values_list('name', flat=True)
        return Response({'tags': tags})

class LogoutView(views.APIView):
    def get(self, request):
        auth_logout(request)
        return Response({'uses':'Logout from session'})
