import django_filters
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, serializers, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title

from .permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsOwnerAdminModeratorOrReadOnly,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignupSerializer,
    TitleSerializer,
    TitleWriteSerializer,
    TokenSerializer,
    UserSerializer,
)


User = get_user_model()

EMAIL_HEADER = "Код подтверждения регистрации на платформе Yamdb."
EMAIL_TEXT = "Ваш одноразовый код подтверждения: {confirmation_code}."
USER_ERROR = "Данные имя пользователя или Email уже зарегистрированы."
CODE_ERROR = "Введен неверный код подтверждения. Запросите новый код."

CONFIRMATION_CODE_LENGTH = 6


class TitleFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(field_name="genre__slug")
    category = django_filters.CharFilter(field_name="category__slug")

    class Meta:
        model = Title
        fields = ["genre", "category", "name", "year"]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"
    http_method_names = ("get", "post", "patch", "delete")
    pagination_class = PageNumberPagination

    @action(
        methods=("get", "patch"),
        detail=False,
        url_path="me",
        permission_classes=(IsAuthenticated,),
    )
    def user_owner(self, request):
        user = request.user
        if request.method == "GET":
            return Response(
                self.get_serializer(user).data, status=status.HTTP_200_OK
            )
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes((AllowAny,))
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data["username"]
    email = serializer.validated_data["email"]
    user, _ = User.objects.get_or_create(username=username, email=email)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        EMAIL_HEADER,
        EMAIL_TEXT.format(confirmation_code=confirmation_code),
        settings.SENDER_EMAIL,
        [user.email],
    )
    user.confirmation_code = confirmation_code
    user.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes((AllowAny,))
def get_token(request):
    """
    Пользователь отправляет свои 'username' и 'confirmation_code'
    на 'auth/token/ и получает токен.
    """
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=request.data["username"])
    if (
        user.confirmation_code != "-" * CONFIRMATION_CODE_LENGTH
        and user.confirmation_code == serializer.data["confirmation_code"]
    ):
        return Response(
            {"token": str(AccessToken.for_user(user))},
            status=status.HTTP_201_CREATED,
        )
    user.confirmation_code = "-" * CONFIRMATION_CODE_LENGTH
    user.save()
    raise serializers.ValidationError(CODE_ERROR)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для обработки эндпоинтов:
    GET DETAIL, GET LIST, POST, PATCH, DELETE
    /titles/{title_id}/reviews/{review_id}/comments/,
    /titles/{titles_id}/reviews/{review_id}/comments/{comment_id}/
    """

    serializer_class = ReviewSerializer
    http_method_names = ("get", "post", "patch", "delete")
    permission_classes = (IsOwnerAdminModeratorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(
            Title,
            id=self.kwargs.get("title_id"),
        )

    def get_queryset(self):
        return self.get_title().reviews.select_related("title", "author")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для обработки эндпоинтов:
    GET DETAIL, GET LIST, POST, PATCH, DELETE
    /titles/{title_id}/reviews/{review_id}/comments/,
    /titles/{titles_id}/reviews/{review_id}/comments/{comment_id}/
    """

    serializer_class = CommentSerializer
    http_method_names = ("get", "post", "patch", "delete")
    permission_classes = (IsOwnerAdminModeratorOrReadOnly,)

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
        )

    def get_queryset(self):
        return self.get_review().comments.select_related("review", "author")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg("reviews__score")).order_by(
        "id"
    )
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleSerializer

        return TitleWriteSerializer


class CategoryGenreBaseViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Абстрактный вьюсет для Жанров и Категорий
    с поддержкой запросв GET LIST, POST, DELETE.
    """

    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    pagination_class = PageNumberPagination
    lookup_field = "slug"
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(CategoryGenreBaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(CategoryGenreBaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
