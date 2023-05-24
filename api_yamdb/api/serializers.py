from django.contrib.auth import get_user_model
from rest_framework import serializers
from reviews.models import Category, Genre, Title

User = get_user_model()


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genre


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    genre = GenresSerializer()
    category = CategoriesSerializer()

    class Meta:
        fields = "__all__"
        model = Title


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username")
