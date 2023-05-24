from django.contrib.auth import get_user_model
from rest_framework import serializers
from reviews.models import Categories, Genres, Title

User = get_user_model()


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Title


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genres


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Categories


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username")
