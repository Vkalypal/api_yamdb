from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import NotLaterThisYearValidator


User = get_user_model()


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
        return self.name[25:] + "..."


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
        validators=(NotLaterThisYearValidator,),
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
        return self.name[25:] + "..."


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

    def __str__(self):
        return f"{self.title} - {self.genre}"


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name="Произведение",
        related_name="reviews",
        on_delete=models.CASCADE,
    )
    text = models.TextField(verbose_name="Отзыв")
    author = models.ForeignKey(
        User,
        verbose_name="Автор отзыва",
        related_name="reviews",
        on_delete=models.CASCADE,
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        validators=(
            MinValueValidator(1, "Оценка не может быть менее 1"),
            MaxValueValidator(10, "Оценка не может быть более 10"),
        ),
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["title"]
        constraints = [
            models.UniqueConstraint(
                name="unique_title_author",
                fields=["title", "author"],
            ),
            models.CheckConstraint(
                check=models.Q(score__gte=1, score__lte=10),
                name='check_score_range',
            ),
        ]

    def __str__(self):
        return self.text[:40] + "..."


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name="Коментарий",
        related_name="comments",
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name="Текст коментария",
    )
    author = models.ForeignKey(
        User,
        verbose_name="Автор коментария",
        related_name="comments",
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации комментария",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["review"]

    def __str__(self):
        return self.text[:40] + "..."
