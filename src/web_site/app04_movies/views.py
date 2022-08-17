from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.generic import \
    View, TemplateView, ListView, UpdateView, DeleteView, DetailView, CreateView
from django.views.generic.base import View
from django.shortcuts import render, redirect

from .models import \
    Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Reviews
from .forms import ReviewsForm, RatingForm

from django.db.models import Q


class GenreYear:
    """ Жанры и года выхода фильмов """
    """ Мы можем наследовать данный класс и затем достать эти данные в 
    шаблонах, этот подход как альтернатива методу get_context_data """

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values('year')

    """ В качестве примера способа используем .values можно вывести не всё а 
    только поле 'year' вывод будет в словаре, а .values_list например возвращает 
    кортеж. Чтобы вывести не в виде словаря нужно к переменной for ещё раз 
    обратиться к полю таблицы year {{ year.year }} (sidebar.html). Смысла
    использования здесь нет, мы всёравно обращаем к полю year в шаблоне, 
    можно удалить .values('year') и всё и так будет работать """


class MoviesView(GenreYear, ListView):
    """ Список фильмов """
    model = Movie
    # Нужно выводить всё кроме черновиков поэтому фильтруем по полю draft
    queryset = Movie.objects.filter(draft=False)  # Не черновик
    paginate_by = 2
    """ paginate_by ограничевает кол-во объектов на странице и добавляет в 
    context этой вьюхи paginator и page_obj"""

    # template_name = 'app04_movies/movie_list.html'
    """ мы не указывали template_name потому что джанга автоматически
    подставляет суфикс к шаблону и будет искать шаблон movie_list
    прилепив к имени модели _list """

    # """ Для того чтобы на странице списка фильмов вывести дополнительно
    # категории в этом классе можно добавить метод get_context_data.
    #  Вызываем метод super нашего родителя, таким образом мы получаем словарь
    #  и заносим его в переменную context, далее добовляем ключ categories
    #  и заносим в него qs(запрос) всех нших категорий, но это говно будет
    #  выводиться только на одной странице этой вьюхи, чтоб это говно не
    #  копировать, в других вьюхах как detail, запиливаем это в темплейт тэг и
    #  грузим его в html header {% load movie_tag %}"""
    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['categories'] = Category.objects.all()
    #     return context


class MovieDetailView(GenreYear, DetailView):
    """ Полное описание фильма """
    model = Movie
    slug_field = 'url'
    """ Указываем slug_field как наше поле url, 
    означает по какому полю будет искать запись, эти данные будут переданы из
    url, сравнивая их с полем slug_field джанго будет искать нужную запись """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        context['form'] = ReviewsForm()
        return context
    """ get_context_data нужна для формы добавления рейтинга, добавляет словарю 
    ещё один ключ star_form и значение заносим форму RatingForm, таким
    образом мы можен обратиться в шаблоне по этому ключу и получить форму
    рейтинга """


class AddReview(View):
    """ Отзывы """

    def post(self, request, pk):
        qs_obj = Movie.objects.get(id=pk)
        form = ReviewsForm(request.POST)  # В форму придут данные из запроса
        if form.is_valid():
            form = form.save(commit=False)  # приостанавливаем сохранение
            """ Ищем ключ parent, это имя скрытого поля для ответа на 
            коммент в форме. Если в запросе будет, то сработает код, если нет то 
            None и проскочит. ПРИВЯЗКА, _id так как будем добавлять число а не 
            объект. parent_id это поле в таблице, Так как значение ключа parent 
            которое мы пролучаем строковое, нужно обернуть его в int. Привязка 
            к этой же таблице """
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            # Тут тоже можно было сделать превязку form.movie_id = form
            form.movie = qs_obj  # Привязка к фильму
            form.save()
        return redirect(qs_obj.get_absolute_url())


class ActorView(GenreYear, DetailView):
    """ Вывод информации о актёре """
    model = Actor
    template_name = 'app04_movies/actor.html'
    slug_field = 'name'  # поле по которому ищем наших актёров


from django import forms


# class FilterForm(forms.Form):
#     name = forms.CharField(
#         required=False,  # IMPORTANT
#         # widget=forms
#     )

class FilterMoviesView(GenreYear, ListView):
    """ Фильтр фильмов """

    paginate_by = 2

    def get_queryset(self):
        list_years = self.request.GET.getlist('year')
        list_genres = self.request.GET.getlist('genre')

        # queryset = Movie.objects.filter(
        #     Q(year__in=list_years) |
        #     Q(genres__in=list_genres)
        # )

        queryset = Movie.objects.filter(draft=False)
        if "year" in self.request.GET:
            queryset = queryset.filter(year__in=list_years)
        if "genre" in self.request.GET:
            queryset = queryset.filter(genres__in=list_genres)
        queryset = queryset.distinct()  # Убираем повторяющиеся элементы

        # kwargs = {}
        # if self.request.GET.getlist("year"):
        #     kwargs["year__in"] = list_years
        # if self.request.GET.getlist("genre"):
        #     kwargs["genres__in"] = list_genres
        #
        # return Movie.objects.filter(draft=False, **kwargs)

        # filtes_form = FilterForm(self.request.GET)
        # _filters = {}
        # if filtes_form.is_valid():
        #     _filters = filtes_form.cleaned_data
        # #
        #
        # _qs_filters = [
        #     Q(draft=False),
        # ]
        # if len(_filters['list_years']) >= 1:
        #     _qs_filters.append(
        #         Q(year__in=filters['list_years'])  # | ....
        #     )
        # #
        # if len(list_genres) >= 1:
        #     _qs_filters.append(
        #         Q(genres__in=list_genres)
        #     )
        # #
        # qs = Movie.objects.filter(
        #     *_qs_filters
        # )

        return queryset

    def get_context_data(self, *args, **kwargs):
        """ Для пагинации"""
        context = super().get_context_data(*args, **kwargs)
        """ В контекст добавим два ключа года и жанры которые будем передавать
         в шаблон и подставлять url пагинации, Так как нам приходит список
          годов и жанров нужно зарание сформировать ссылку чтоб в шаблоне её 
          подставлять и не перебирать циклов for """
        """ Формируем строку из элементов списка соединяем их (join). В join
        передаём генератор списка который формирует строку состоящую из года
        и того элемента который пришёл и знак &. Так м генерируем строку
        которая является один элемент списка далее список разложен в строку """
        context['year'] = ''.join(
            [f'year={x}&' for x in self.request.GET.getlist('year')]
        )
        context['genre'] = ''.join(
            [f'genre={x}&' for x in self.request.GET.getlist('genre')]
        )
        return context



    """ Фильтр там где года (будут входить - __in) в список который будет 
    возвращаться с фронтэнда, это список годов. 
    Т.е. с помощью метода .getlist достаём из запроса .GET список годов """


# class JsonFilterMoviesView(ListView):
#     """ Фильтр фильмов в json """
#
#     # def get_queryset(self):
#     #     queryset = Movie.objects.filter(
#     #         Q(year__in=self.request.GET.getlist('year')) |
#     #         Q(genres__in=self.request.GET.getlist('genre'))
#     #     ).distinct().values('title', 'tagline', 'url', 'poster')
#     #     """ С помощью .distinct исключаем повторения и указываем в каких
#     #     полях"""
#     #
#     #     return queryset
#
#     def get_queryset(self):
#
#         list_years = self.request.GET.getlist('year')
#         list_genres = self.request.GET.getlist('genre')
#
#         queryset = Movie.objects.filter(draft=False)
#         if "year" in self.request.GET:
#             queryset = queryset.filter(year__in=list_years)
#         if "genre" in self.request.GET:
#             queryset = queryset.filter(genres__in=list_genres)
#
#         queryset = queryset.distinct().values(
#             'title', 'tagline', 'url', 'poster'
#         )
#         """ С помощью .distinct исключаем повторения и указываем в каких
#         полях """
#
#         return queryset
#
#     def get(self, request, *args, **kwargs):
#         queryset = list(self.get_queryset())
#         return JsonResponse({'movies': queryset}, safe=False)
#     """ Приве get запросе (def get) пихаем в список фильрованное говно
#     и передаём словарём в ключе movies """


class AddStarRating(View):
    """ Добавление рейтинга фильму """

    def get_client_ip(self, request):
        """ Тут получаем ip адрес клиента который отправил нам запрос """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    """ Когда пидёт post запрос в форму RatingForm мы передаём ей request.POST
    таким образом сгенерируется форма """
    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            """ Так как один клиент не может установить разный рейтинг фильму
            т.е. если запитсь уже была создана, то при следущем добавлении
            или именении нужно её изменить а не создавать ещё одну.
            # В ip пихпем нашу функцию выше где получаем ip адрес клиента.
            В поле movie_id передаём поле move из POST запроса и оборачиваем 
            в int чтобы было числовое значение, эти данные приходт со скрытого 
            поля movie в movie_detail.html. В defaults передаём словарь с 
            ключём того поля которое хотим изменить и значение на которое 
            меняем в том случе если найдём такую запись, это поле star_id
            в которое будем передавать star из POST запроса и так же оборачиваем
            в int. т.е. это поле radio значение самой звезды, если такая 
            запись найдета обновится только поле star_id, т.е. привязываемся 
            к другой звизде и пользователь может менять тот рейтинг который 
            он устанавливает фильму. 
            В конце возвращаем статус в зависимости валидна ли была форма """
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),  # В ip пихпем нашу функцию выше
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
        """ Фильтруем запрос в поиск по полю title в фильмах, с использованием
        __icontains чтобы не учитывался регистр, .strip() убераем пробелы """
        return Movie.objects.filter(
            title__icontains=self.request.GET.get('search').strip()
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        """ В контекст добавляем то значение что пришло с поисковика, 
        для того чтоб работала пагинация """
        context['search'] = f'search={self.request.GET.get("search")}&'
        return context
