from django.urls import path
from .views import TagList
from rest_framework_simplejwt.views import TokenObtainPairView
from .routers import router_user, router_article


urlpatterns = router_user.urls
urlpatterns += router_article.urls
urlpatterns += [
    path('tags/', TagList.as_view()),
    path('users/login/', TokenObtainPairView.as_view()),
]


