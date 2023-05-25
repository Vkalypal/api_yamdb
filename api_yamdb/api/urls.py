from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, GenreViewSet, SignUpViewSet,
                    TitleViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register(r"titles", TitleViewSet, basename="titles")
router_v1.register(r"categories", CategoryViewSet, basename="categories")
router_v1.register(r"genres", GenreViewSet, basename="genres")


urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v1/", include("djoser.urls")),
    path("v1/auth/signup/", SignUpViewSet.as_view(), name="signup"),
]
