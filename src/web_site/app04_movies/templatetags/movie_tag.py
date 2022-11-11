from django import template
from app04_movies.models import Category, Movie

register = template.Library()

@register.simple_tag()
def get_categories():
    """ Вывод всех категорий """
    return Category.objects.all()


@register.inclusion_tag('app04_movies/tags/last_movie.html')
def get_last_movies(count=5):
    """ Вывод последних фильмов """
    # Фильтруем без черновиков, сортировка по id, срез первые 5 записей
    movies = Movie.objects.filter(draft=False).order_by('id')[:count]
    return {"last_movies": movies}
