from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import \
    Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Reviews

from ckeditor_uploader.widgets import CKEditorUploadingWidget

admin.site.site_title = 'Django administration '
admin.site.site_header = 'Django administration '


class MovieAdminForm(forms.ModelForm):
    """ Виджет текстового редактора, с возможностью загрузки файлов """
    description = forms.CharField(
        label='Описание',
        widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Категории """
    list_display = ('id', 'name', 'url')
    list_display_links = ('name',)


class ReviewInline(admin.TabularInline):
    """ Отзывы на странице фильма """
    model = Reviews
    readonly_fields = ('name', 'email')
    extra = 1
    """ При открытии записи фильма видем дополнительно все отзывы к нему """


class MovieShotsInline(admin.TabularInline):
    """ Кадры из фильма на странице фильма """
    model = MovieShots
    extra = 1

    """ Миниатюры изображений """
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="220" height="150"')

    get_image.short_description = 'Изображение'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """ Фильмы """
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__name')
    inlines = [MovieShotsInline, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ('draft',)
    form = MovieAdminForm  # Виджет текстового редактора
    actions = ['publish', 'unpublish']
    fieldsets = [
        (None, {
            'fields': (('title',),)
        }),
        (None, {
            'fields': ('description', ('poster', 'trailer'),)
        }),
        (None, {
            'fields': (('year', 'world_premiere', 'country'),)
        }),
        ('Actors', {
            # 'classes': ('collapse',),
            'fields': (('actors', 'directors', 'genres', 'category'),)
        }),
        (None, {
            'fields': (('seasons', 'series'),)
        }),
        ('Options', {
            'fields': (('url', 'draft'),)
        })
    ]

    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="150" height="200"')
    get_image.short_description = 'Постер'

    def unpublish(self, request, queryset):
        """ Снять с публикации """
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = ('change',)

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
    readonly_fields = ('name', 'email')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """ Жанры """
    list_display = ('name', 'url')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """ Актёры """
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image',)

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
