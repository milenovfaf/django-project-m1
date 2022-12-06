from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.shortcuts import redirect

from .models import Genre, Movie, Actor, Rating
from .forms import ReviewsForm, RatingForm
from .service import get_client_ip


class GenreYear:
    """ Жанры и года выхода фильмов """

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False)


class MoviesView(GenreYear, ListView):
    """ Список фильмов """
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    paginate_by = 1

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['categories'] = Category.objects.all()
    #     return context


class MovieDetailView(GenreYear, DetailView):
    """ Полное описание фильма """
    model = Movie
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        context['form'] = ReviewsForm()
        return context


class AddReview(View):
    """ Отзывы """
    def post(self, request, pk):
        qs_obj = Movie.objects.get(id=pk)
        form = ReviewsForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = qs_obj
            form.save()
        return redirect(qs_obj.get_absolute_url())


class ActorView(GenreYear, DetailView):
    """ Вывод информации о актёре """
    model = Actor
    template_name = 'app04_movies/actor.html'
    slug_field = 'name'


class FilterMoviesView(GenreYear, ListView):
    """ Фильтр по годам и жанрам """
    paginate_by = 4

    def get_queryset(self):
        list_years = self.request.GET.getlist('year')
        list_genres = self.request.GET.getlist('genre')

        # queryset = Movie.objects.filter(
        #     Q(year__in=list_years) |
        #     Q(genres__in=list_genres)
        # ).distinct().values('title', 'url', 'poster')

        queryset = Movie.objects.filter(draft=False)
        if "year" in self.request.GET:
            queryset = queryset.filter(year__in=list_years)
        if "genre" in self.request.GET:
            queryset = queryset.filter(genres__in=list_genres)
        queryset = queryset.distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        """ Пагинация """
        context = super().get_context_data(*args, **kwargs)
        context['year'] = ''.join(
            [f'year={x}&' for x in self.request.GET.getlist('year')]
        )
        context['genre'] = ''.join(
            [f'genre={x}&' for x in self.request.GET.getlist('genre')]
        )
        return context


class AddStarRating(View):
    """ Добавление рейтинга фильму """

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=get_client_ip(request),
                movie_id=int(request.POST.get('movie')),
                defaults={'star_id': int(request.POST.get('star'))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class Search(ListView):
    """ Поиск фильмов """
    paginate_by = 2

    def get_queryset(self):
        return Movie.objects.filter(
            title__icontains=self.request.GET.get('search').strip()
        )

    def get_context_data(self, *args, **kwargs):
        """ Пагинация """
        context = super().get_context_data(*args, **kwargs)
        context['search'] = f'search={self.request.GET.get("search")}&'
        return context
