from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import validate_username, validate_year


USER = "user"
ADMIN = "admin"
MODERATOR = "moderator"

ROLE_CHOICES = (
    (USER, "Пользователь"),
    (MODERATOR, "Модератор"),
    (ADMIN, "Администратор"),
)


class User(AbstractUser):
    """Кастомная модель пользователя."""

    username = models.CharField(
        verbose_name="Имя пользователя",
        validators=(validate_username,),
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        verbose_name="Электронная почта",
        max_length=254,
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
        verbose_name="Имя", max_length=150, blank=True
    )
    last_name = models.CharField(
        verbose_name="Фамилия", max_length=150, blank=True
    )
    confirmation_code = models.CharField(max_length=6, default="-" * 6)

    @property
    def is_user(self):
        """Обычный пользователь."""
        return self.role == USER

    @property
    def is_admin(self):
        """Пользователь с правами администратора."""
        return self.role == ADMIN or self.is_staff

    @property
    def is_moderator(self):
        """Пользователь с правами модератора."""
        return self.role == MODERATOR

    class Meta:
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username[:15]


class Category(models.Model):
    name = models.CharField(verbose_name="Название категории", max_length=256)
    slug = models.SlugField(
        verbose_name="Слаг категории", max_length=50, unique=True
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(verbose_name="Название жанра", max_length=256)
    slug = models.SlugField(
        verbose_name="Слаг жанра", max_length=50, unique=True
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ["name"]

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(verbose_name="Наименование", max_length=256)
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

    def __str__(self):
        return f"{self.title} - {self.genre}"


class FeedbackModel(models.Model):
    """Родительский класс для отзывов и комментариев."""

    FEEDBACK = "{text:.15} username: {author} " "дата публикации: {pub_date}"

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

    ERROR_SCORE_MIN_MAX = f"Допустимы значения от {1} до {10}"

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name="Произведение"
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        validators=[
            MinValueValidator(1, ERROR_SCORE_MIN_MAX),
            MaxValueValidator(10, ERROR_SCORE_MIN_MAX),
        ],
    )

    class Meta(FeedbackModel.Meta):
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = (
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_title"
            ),
        )


class Comment(FeedbackModel):
    """Комментарии пользователей."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name="Отзыв"
    )

    class Meta(FeedbackModel.Meta):
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
