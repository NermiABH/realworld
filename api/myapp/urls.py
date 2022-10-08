from django.urls import path, re_path
from .views import ArticleViewSet, TagList
from rest_framework.routers import SimpleRouter

router_article = SimpleRouter()
router_article.register(r'articles', ArticleViewSet)

urlpatterns = router_article.urls

urlpatterns += [
    path('tags', TagList.as_view())
]


