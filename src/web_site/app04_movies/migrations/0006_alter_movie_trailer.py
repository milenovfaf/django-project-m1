# Generated by Django 3.2.15 on 2022-09-19 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app04_movies', '0005_auto_20220919_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='trailer',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Трейлер'),
        ),
    ]
