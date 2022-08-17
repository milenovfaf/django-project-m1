from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import \
    Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Reviews

admin.site.site_title = 'Слава Джанге'
admin.site.site_header = 'Слава Джанге'

####################################

""" pip install django-ckeditor - Текстовый редактор для джанго админ панельи, 
с мудрёной установкой"
https://www.youtube.com/watch?v=fMZBTCRGMS8&list=PLF-NY6ldwAWrb6nQcPL21XX_-AmivFAYq&index=15"""

from ckeditor_uploader.widgets import CKEditorUploadingWidget

""" Виджет Тектового редактора, с возможностью загрузки файлов. Полю которое 
отвечает за описание фольма мы добавляем CharField и прописываем виджет для
этого поля, таким образов административной панели мы увидит редактор, затем 
данную форму нужно подлючить к класу, т.е. в классе MoveAdmin добавляем 
атрибут form и присваиваем ему нашу форму form = MovieAdminForm """


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(
        label='Описание',
        widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'

#####################################


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Категории """
    list_display = ('id', 'name', 'url')
    list_display_links = ('name',)  # Так имя категории это ссылка


class ReviewInline(admin.TabularInline):
    """ Отзывы на странице фильма """
    model = Reviews
    readonly_fields = ('name', 'email')  # Нельзя редактировать
    extra = 1  # кол-во дополнительных пустых полей, если не указывать то их 3
    """ При открытии записи фильма видем дополнительно все отзывы к нему
    StackedInline - поля коментов выводятся друг под друга, а если  
    TabularInline - то по горизонтали, в классе MoveAdmin мы крепим этот класс
    inlines = [ReviewInline], работает с ForeignKey, MtM """


class MovieShotsInline(admin.TabularInline):
    """ Кадры из фильма на странице фильма """
    model = MovieShots
    extra = 1
    """ Покажим миниатюры """
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="220" height="150"')

    get_image.short_description = 'Изображение'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """ Фильмы """
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year')
    # __name - по какому именно полю искать
    search_fields = ('title', 'category__name')
    """ В inlines крепим верхние классы """
    inlines = [MovieShotsInline, ReviewInline]
    save_on_top = True  # Здесь мы дублируем кнопки save в верху
    save_as = True
    """ save_as менят кнопку чтоб заного не заполнять поля после добавления 
    записи, а просто редактировать нужные для следующей"""
    list_editable = ('draft',)  # можно редакт в списке фильмов (галку ставить)
    form = MovieAdminForm  # Подключили класс виджета редатора
    actions = ['publish', 'unpublish']

    # fields = (('actors', 'directors', 'genre'),)
    """ Какие поля показать и доп скобки, делают в одну строку"""

    """ Так выводятся только нужные поля, а чтобы были в одну строку надо 
    ('title', 'tagline'), засунуть в ещё один кортеж (('title', 'tagline'),) 
    с помощью fieldsets групперуем поля, на месте None можно задать имя 
    группы, а при добавлении в словарь 'classes': ('collapse',) группа 
    становится сворачиваемая """
    fieldsets = [
        (None, {
            'fields': (('title', 'tagline'),)
        }),
        (None, {
            'fields': ('description', ('poster', 'get_image')),
        }),
        (None, {
            'fields': (('year', 'world_premiere', 'country'),)
        }),
        ('Actors', {
            'classes': ('collapse',),
            'fields': (('actors', 'directors', 'genres', 'category'),)
        }),
        (None, {
            'fields': (('budget', 'fees_in_usa', 'fess_in_world'),)
        }),
        ('Options', {
            'fields': (('url', 'draft'),)
        })
    ]
    readonly_fields = ('get_image',)
    """ Добавлено отображение миниатюры постера, get_image указан в 
    readonly_fields и в том месте где их показать в группе полей ('description',
     'poster', 'get_image') """

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="150" height="200"')
    get_image.short_description = 'Постер'

    """ Экшины publish и unpublish появятся в выподающем меню раздела фильмы 
    в списке действий """

    def unpublish(self, request, queryset):
        """ Снять с публикации """
        row_update = queryset.update(draft=True)  # черновик вкл
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = ('change',)

    """ Что бы применять данные экшины у пользователя должны быть права на 
    редактирование записи за это отвечат allowed_permissions = ('change',) """

    def publish(self, request, queryset):
        """ Опубликовать """
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change',)


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    """ Отзывы """
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ('name', 'email')  # Нельзя редактировать


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """ Жанры """
    list_display = ('name', 'url')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """ Актёры """
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image',)

    """ Покажим миниатюры изображений, а не просто ссылки. Пишем метод 
    get_image который принимает объект (obj) модели Actor, и возращает работу 
    импортированного метода mark_safe, который выведет html не как строку 
    а как тег. А с помощью short_description ниже указываем как будет 
    называться столбец, затем в list_display добавляем имя нашего метода,
    а указав го в readonly_fields, миниатюра отобразится и на самой странице
    редактирования. То же применили к кадрам для фильма"""

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = 'Изображение'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """ Рейтинг """
    list_display = ('star', 'movie', 'ip')


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    """ Звезда рейтинга """
    list_display = ('value',)


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """ Кадры из фильма """
    list_display = ('title', 'image', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="90" height="60"')

    get_image.short_description = 'Изображение'
