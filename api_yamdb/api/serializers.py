from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


User = get_user_model()


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Title


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Category


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username")


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    class Meta:
        model = Review
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = "__all__"
