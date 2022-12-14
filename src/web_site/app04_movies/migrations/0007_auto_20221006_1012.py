# Generated by Django 3.2.15 on 2022-10-06 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app04_movies', '0006_alter_movie_trailer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actor',
            options={'default_related_name': 'genres', 'verbose_name': 'Актёры и режиссёры', 'verbose_name_plural': 'Актёры и режиссёры'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'default_related_name': 'actors', 'verbose_name': 'Жанр', 'verbose_name_plural': 'Жанры'},
        ),
        migrations.AlterIndexTogether(
            name='movie',
            index_together={('url',)},
        ),
    ]
