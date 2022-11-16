from rest_framework import routers
from django.urls import include, path
from .views import RegisterView,VerifyUserView


router_v1 = routers.DefaultRouter()
router_v1.register('auth/signup', RegisterView, basename='signup')



urlpatterns = [
    path('api/v1/', include(router_v1.urls)),
    path('api/v1/auth/token/', VerifyUserView.as_view(), name='token')
]
