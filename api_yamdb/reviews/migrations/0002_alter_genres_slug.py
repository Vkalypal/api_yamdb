# Generated by Django 3.2 on 2023-05-23 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genres',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Название жанра'),
        ),
    ]