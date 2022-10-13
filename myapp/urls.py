from django.urls import path
from .views import TagList
from rest_framework_simplejwt.views import TokenObtainPairView
from .routers import router_article
from .views import UserCustomViewSet

urlpatterns = router_article.urls
urlpatterns += [
    path('tags/', TagList.as_view()),
    path('users/login/', TokenObtainPairView.as_view()),
    path('users/', UserCustomViewSet.as_view({'post':'create'})),
    path('user/', UserCustomViewSet.as_view({'get':'me',
                                       'put': 'me',
                                       'patch': 'me'})),
    path('profiles/<str:username>/', UserCustomViewSet.as_view({'get':'retrieve'})),
    path('profiles/<str:username>/follow/', UserCustomViewSet.as_view({'get':'follow_profile'})),


    path('all_users/', UserCustomViewSet.as_view({'get':'list'}))
]


