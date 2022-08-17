from django import template
from app04_movies.models import Category, Movie

register = template.Library()

""" Создаём функцию которая будет возвращать список категорий, вся эта залупа 
нужна чтобы не повторять метот вывода списка категорий в heder в каждой вьюхе 
для каждой странице, лучше наследовать html как в варианте с app01_products,
зато мы теперь знаем что такое темплэйт тэги, по мимо темплейт тэгов такую
задачу можно решить с помощью миксин класа которого наследуют другие вьюхи.
https://www.youtube.com/watch?v=_do8WT4z_7I&list=PLF-NY6ldwAWrb6nQcPL21XX_-AmivFAYq&index=17 """


@register.simple_tag()
def get_categories():
    """ Вывод всех категорий """
    return Category.objects.all()


""" Существует два вида темплэйт тэгов это simple_tag и inclusion_tag, отличие в 
том что inclusion_tag умеет рендерить шаблон, им и будем рендерить список
 последних фильмов, запихав этот кусок html из sidebar в отдельный шаблон """


# @register.inclusion_tag('app04_movies/tags/last_movie.html')
# def get_last_movies():
#     """ Вывод последних фильмов """
#     # Фильтруем без черновиков, сортировка по id, срез первые 5 записей
#     movies = Movie.objects.filter(draft=False).order_by('id')[:5]
#     return {"last_movies": movies}


""" В этом варианте выводятся не просто 5 последних, а можно передавать
 аргумент в шаблоне sidebar куда была вставлена эта функция (тэг) указав 
 колличество count=2 например, и функция подставит переданное число в срез 
 списка """


@register.inclusion_tag('app04_movies/tags/last_movie.html')
def get_last_movies(count=5):
    """ Вывод последних фильмов """
    # Фильтруем без черновиков, сортировка по id, срез первые 5 записей
    movies = Movie.objects.filter(draft=False).order_by('id')[:count]
    return {"last_movies": movies}
