from rest_framework import routers
from .views import ArticleViewSet


class ArticleRouter(routers.SimpleRouter):
    routes = [
        routers.Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        routers.Route(
            url=r'^{prefix}/feed{trailing_slash}$',
            mapping={
                'get': 'list_feed',
            },
            name='{basename}-list_feed',
            detail=False,
            initkwargs={'suffix': 'List'}
        )
    ]


router_article = ArticleRouter()
router_article.register('articles', ArticleViewSet)

