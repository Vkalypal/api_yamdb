from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from reviews.validators import validate_username


User = get_user_model()

ERROR_REPEAT_REVIEW = 'Вы уже оставляли отзыв на это произведение'


class UserSerializer(serializers.ModelSerializer):
    """Сериализация данных пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_username(self, value):
        validate_username(value)
        return value


class SignupSerializer(serializers.Serializer):
    """Сериализация данных пользователя при регистрации."""
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=(validate_username,)
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
    )


class TokenSerializer(serializers.Serializer):
    """Сериализация данных для получения токена."""
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=(validate_username,)
    )
    confirmation_code = serializers.CharField(
        required=True,
        max_length=6
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
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = "__all__"
        model = Title


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = "__all__"
        model = Title

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category', 'rating')

    def get_rating(self, instance):
        reviews = Review.objects.filter(title=instance)
        if reviews.exists():
            total_scores = sum(review.score for review in reviews)
            average_score = total_scores / reviews.count()
            return average_score
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['genre'] = GenreSerializer(instance.genre.all(), many=True).data
        data['category'] = CategorySerializer(instance.category).data
        return data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field="username",
        read_only=True,
    )

    def validate(self, data):
        if self.context["request"].method == "POST":
            title_id = self.context['request'].parser_context["kwargs"][
                "title_id"
            ]
            if Review.objects.filter(
                author=self.context["request"].user, title_id=title_id
            ).exists():
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
