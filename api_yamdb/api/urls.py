from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import SignUpViewSet

urlpatterns = [
    path('v1/', include('djoser.urls')),
    path('v1/auth/signup/', SignUpViewSet.as_view(), name='signup'),
]