from rest_framework import routers
from .views import UserViewSet
from rest_framework.routers import SimpleRouter
from .views import ArticleCommentViewSet

class UserRouter(routers.SimpleRouter):
    routes = [
        routers.Route(
            url=r'^{prefix}s{trailing_slash}$',
            mapping={
                'post': 'create'
            },
            name='{basename}s-create',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        routers.Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update'
            },
            name='{basename}s-current',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        routers.DynamicRoute(
            url=r'^{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
    ]

router_user = UserRouter()
router_user.register(r'user', UserViewSet)
router_article = SimpleRouter()
router_article.register(r'articles', ArticleCommentViewSet)
