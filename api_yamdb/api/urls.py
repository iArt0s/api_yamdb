from rest_framework import routers
from django.urls import include, path
from .views import (RegisterView, VerifyUserView, CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    UserViewSet, SelfUserViewSet
)


router_v1=routers.DefaultRouter()
router_v1.register('auth/signup', RegisterView, basename = 'signup')
router_v1.register(r'genres', GenreViewSet, basename = 'genres')
router_v1.register(r'categories', CategoryViewSet, basename = 'categories')
router_v1.register(r'titles', TitleViewSet, basename = 'titles')
router_v1.register('users',UserViewSet, basename = 'users')
router_v1.register(r'me',SelfUserViewSet, basename = 'me')



urlpatterns=[
    path('api/v1/', include(router_v1.urls)),
    path('api/v1/auth/token/', VerifyUserView.as_view(), name='token')
]
