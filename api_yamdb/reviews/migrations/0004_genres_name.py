# Generated by Django 3.2 on 2023-05-23 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20230523_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='genres',
            name='name',
            field=models.CharField(default='none', max_length=200),
        ),
    ]
