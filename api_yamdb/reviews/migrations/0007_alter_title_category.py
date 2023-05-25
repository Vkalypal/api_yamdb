# Generated by Django 3.2 on 2023-05-24 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_auto_20230524_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(default='Без категории', on_delete=django.db.models.deletion.SET_DEFAULT, to='reviews.category', unique=True),
        ),
    ]
