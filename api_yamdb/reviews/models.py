from django.db import models

from reviews.validators import NotLaterThisYearValidator


class Category(models.Model):
    name = models.CharField(verbose_name="Название категории", max_length=256)
    slug = models.SlugField(verbose_name="Слаг категории", max_length=50, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(verbose_name="Название жанра", max_length=256)
    slug = models.SlugField(verbose_name="Слаг жанра", max_length=50, unique=True)

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
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    genre = models.ManyToManyField(
        Genre,
        verbose_name="Жанр",
        through="GenreTitle",
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        related_name="titles",
        on_delete=models.SET_NULL,
        null=True,
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

    def __str__(self):
        return f"{self.title} - {self.genre}"
