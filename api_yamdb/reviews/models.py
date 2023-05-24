from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name="Название категории", max_length=200)
    slug = models.SlugField(verbose_name="Слаг категории", unique=True)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(verbose_name="Название жанра", max_length=200)
    slug = models.SlugField(verbose_name="Слаг жанра", unique=True)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.name
