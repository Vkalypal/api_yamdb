from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from reviews.models import Categories, Genres, Title

from .serializers import (
    CategoriesSerializer,
    GenresSerializer,
    SignUpSerializer,
    TitleSerializer,
)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class GenresViewSet(ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class CategoriesViewSet(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class SignUpViewSet(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_mail(
                "Тема письма",
                "Текст письма.",
                "practicum29team@mail.ru",
                [serializer.validated_data["email"]],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
