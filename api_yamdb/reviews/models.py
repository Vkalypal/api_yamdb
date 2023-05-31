from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import validate_username, validate_year


class User(AbstractUser):
    """Кастомная модель пользователя."""

    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"

    ROLE_CHOICES = (
        (USER, "Пользователь"),
        (MODERATOR, "Модератор"),
        (ADMIN, "Администратор"),
    )

    USERNAME_MAX_LENGTH = 150
    EMAIL_MAX_LENGTH = 254
    FIRST_NAME_MAX_LENGTH = 150
    FIRST_NAME_MAX_OUTPUT_LENGTH = 15
    LAST_NAME_MAX_LENGTH = 150
    CONFIRMATION_CODE_LENGTH = 6

    username = models.CharField(
        verbose_name="Имя пользователя",
        validators=(validate_username,),
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
    )
    email = models.EmailField(
        verbose_name="Электронная почта",
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
    )
    role = models.CharField(
        verbose_name="Роль",
        max_length=max(len(role) for role, _ in ROLE_CHOICES),
        choices=ROLE_CHOICES,
        default=USER,
        blank=True,
    )
    bio = models.TextField(
        verbose_name="Биография",
        blank=True,
    )
    first_name = models.CharField(
        verbose_name="Имя", max_length=FIRST_NAME_MAX_LENGTH, blank=True
    )
    last_name = models.CharField(
        verbose_name="Фамилия", max_length=LAST_NAME_MAX_LENGTH, blank=True
    )
    confirmation_code = models.CharField(
        max_length=CONFIRMATION_CODE_LENGTH,
        default="-" * CONFIRMATION_CODE_LENGTH,
    )

    @property
    def is_user(self):
        """Обычный пользователь."""
        return self.role == User.USER

    @property
    def is_admin(self):
        """Пользователь с правами администратора."""
        return self.role == User.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        """Пользователь с правами модератора."""
        return self.role == User.MODERATOR

    class Meta:
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username[: User.FIRST_NAME_MAX_OUTPUT_LENGTH]


class Category(models.Model):
    NAME_MAX_LENGTH = 256
    SLUG_MAX_LENGTH = 50

    name = models.CharField(
        verbose_name="Название категории", max_length=NAME_MAX_LENGTH
    )
    slug = models.SlugField(
        verbose_name="Слаг категории", max_length=SLUG_MAX_LENGTH, unique=True
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Genre(models.Model):
    NAME_MAX_LENGTH = 256
    SLUG_MAX_LENGTH = 50

    name = models.CharField(
        verbose_name="Название жанра", max_length=NAME_MAX_LENGTH
    )
    slug = models.SlugField(
        verbose_name="Слаг жанра", max_length=SLUG_MAX_LENGTH, unique=True
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ["name"]

    def __str__(self):
        return self.slug


class Title(models.Model):
    NAME_MAX_LENGTH = 256

    name = models.CharField(
        verbose_name="Наименование", max_length=NAME_MAX_LENGTH
    )
    year = models.IntegerField(
        verbose_name="Год",
        db_index=True,
        validators=(validate_year,),
    )
    description = models.TextField(
        verbose_name="Описание", null=True, blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name="Жанр",
        through="GenreTitle",
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        related_name="titles",
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ["name"]

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name="Произведение",
        related_name="genres",
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        verbose_name="Жанр",
        related_name="titles",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} - {self.genre}"


class FeedbackModel(models.Model):
    """Родительский класс для отзывов и комментариев."""

    TEXT_MAX_OUTPUT_LENGTH = 15
    FEEDBACK = (
        "{text:.TEXT_MAX_OUTPUT_LENGTH} "
        "username: {author} дата публикации: {pub_date}"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Aвтор",
    )
    text = models.TextField(
        verbose_name="Текст",
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ("-pub_date",)
        default_related_name = "%(class)ss"

    def __str__(self):
        return self.FEEDBACK.format(
            text=self.text,
            author=self.author.username,
            pub_date=self.pub_date,
        )


class Review(FeedbackModel):
    """Отзывы пользователей."""

    MIN_SCORE = 1
    MAX_SCORE = 10
    ERROR_SCORE_MIN_MAX = f"Допустимы значения от {MIN_SCORE} до {MAX_SCORE}"

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name="Произведение"
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        validators=[
            MinValueValidator(MIN_SCORE, ERROR_SCORE_MIN_MAX),
            MaxValueValidator(MAX_SCORE, ERROR_SCORE_MIN_MAX),
        ],
    )

    class Meta(FeedbackModel.Meta):
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ("title",)
        constraints = (
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_title"
            ),
        )

    def __str__(self):
        return f"{self.title} - оценка: {self.score}"


class Comment(FeedbackModel):
    """Комментарии пользователей."""

    REVIEW_MAX_OUTPUT_LENGTH = 15

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name="Отзыв"
    )

    class Meta(FeedbackModel.Meta):
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.review[: Comment.REVIEW_MAX_OUTPUT_LENGTH]
