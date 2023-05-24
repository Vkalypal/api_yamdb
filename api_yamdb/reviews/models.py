from django.db import models


class Categories(models.Model):
    name = models.CharField(verbose_name="Название категории", max_length=200)
    slug = models.SlugField(verbose_name="Слаг категории", unique=True)

    def __str__(self):
        return self.slug


class Genres(models.Model):
    name = models.CharField(verbose_name="Название жанра", max_length=200)
    slug = models.SlugField(verbose_name="Слаг жанра", unique=True)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(blank=True)
    genre = models.ForeignKey(Genres, on_delete=models.SET_DEFAULT, default="Без жанра")
    category = models.OneToOneField(
        Categories, on_delete=models.SET_DEFAULT, default="Без категории"
    )

    def __str__(self):
        return self.name
