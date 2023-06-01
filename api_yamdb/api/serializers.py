from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from reviews.validators import validate_username


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализация данных пользователя."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )

    def validate_username(self, value):
        validate_username(value)
        return value


class SignupSerializer(serializers.Serializer):
    """Сериализация данных пользователя при регистрации."""

    USERNAME_MAX_LENGTH = 150
    EMAIL_MAX_LENGTH = 254

    username = serializers.CharField(
        required=True,
        max_length=USERNAME_MAX_LENGTH,
        validators=(validate_username,),
    )
    email = serializers.EmailField(
        required=True,
        max_length=EMAIL_MAX_LENGTH,
    )

    def validate(self, data):
        if User.objects.filter(username=data["username"]).exists():
            email = User.objects.get(username=data["username"]).email
            if email != data["email"]:
                raise serializers.ValidationError("Неправильный email")
        if User.objects.filter(email=data["email"]).exists():
            username = User.objects.get(email=data["email"]).username
            if username != data["username"]:
                raise serializers.ValidationError("Неправильный username")
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализация данных для получения токена."""

    USERNAME_MAX_LENGTH = 150
    CODE_MAX_LENGTH = 6

    username = serializers.CharField(
        required=True,
        max_length=USERNAME_MAX_LENGTH,
        validators=(validate_username,),
    )
    confirmation_code = serializers.CharField(
        required=True, max_length=CODE_MAX_LENGTH
    )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Category


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )

    class Meta:
        fields = "__all__"
        model = Title


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.FloatField()

    class Meta:
        fields = "__all__"
        model = Title

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
            "rating",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["genre"] = GenreSerializer(instance.genre.all(), many=True).data
        data["category"] = CategorySerializer(instance.category).data
        data["rating"] = instance.rating
        return data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field="username",
        read_only=True,
    )

    def validate(self, data):
        if self.context["request"].method == "POST":
            title_id = self.context["request"].parser_context["kwargs"][
                "title_id"
            ]
            title = get_object_or_404(Title, pk=title_id)
            author = self.context["request"].user
            if title.reviews.select_related("title").filter(author=author):
                raise serializers.ValidationError(
                    "Публиковать более одного обзора на одно и то же "
                    "произведение нельзя! "
                )
        return data

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field="username",
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
