from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import SignUpViewSet, UsersViewSet, get_token


router = DefaultRouter()
router.register(
    'users',
    UsersViewSet,
    basename='users'
)
urlpatterns = [
    path('v1/auth/token/', get_token),
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignUpViewSet.as_view(), name='signup'),
]