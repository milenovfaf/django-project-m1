from datetime import date
from django.db import models
from django.urls import reverse


class Category(models.Model):
    """ Категории """
    name = models.CharField('Категория', max_length=150)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Actor(models.Model):
    """ Актёры и режиссёры """
    name = models.CharField('Имя', max_length=100)
    age = models.PositiveSmallIntegerField('Возраст', default=0)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='actors/')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor-detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = 'Актёры и режиссёры'
        verbose_name_plural = 'Актёры и режиссёры'


class Genre(models.Model):
    """ Жанры """
    name = models.CharField('Имя', max_length=100)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Movie(models.Model):
    """ Фильмы """
    title = models.CharField("Название", max_length=100)
    tagline = models.CharField("Слоган", max_length=100, default='')
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Дата выхода", default=2019)
    country = models.CharField("Страна", max_length=30)

    directors = models.ManyToManyField(
        Actor,
        verbose_name="режиссер",
        related_name="film_director")
    actors = models.ManyToManyField(
        Actor,
        verbose_name="актеры",
        related_name="film_actor")
    genres = models.ManyToManyField(
        Genre,
        verbose_name="жанры")

    world_premiere = models.DateField("Примьера в мире", default=date.today)
    budget = models.PositiveIntegerField(
        "Бюджет", default=0, help_text="указывать сумму в долларах")
    fees_in_usa = models.PositiveIntegerField(
        "Сборы в США", default=0, help_text="указывать сумму в долларах"
    )
    fess_in_world = models.PositiveIntegerField(
        "Сборы в мире", default=0, help_text="указывать сумму в долларах"
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.SET_NULL,
        null=True
    )  # Если удалить поле станет NULL и True указываем что поле может быть null

    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("Черновик", default=False)  # Черновик

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Указываем имя и параметры в словаре, которые передаём в url
        return reverse("movie-detail", kwargs={"slug": self.url})

    """ Метод get_review возвращает список отзывов прикреплённых к фильму, 
    фильтрует так где поле parent будет равно null, таким образум вернутся
    только родительские отзывы к нашему фильму"""
    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class MovieShots(models.Model):
    """Кадры из фильма"""
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="movie_shots/")

    movie = models.ForeignKey(
        Movie,
        verbose_name="Фильм",
        on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильма"


class RatingStar(models.Model):
    """ Звезда рейтинга """
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'
        # Преобразов в строку иначе выйдет ошибка при добавлении числа в админке

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]  # сортировка по полю чтоб звёзды от > к < отобр


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)  # Кто добавил рейтинг

    star = models.ForeignKey(  # привязка к значению звезды котор выбрал юзер
        RatingStar,
        on_delete=models.CASCADE,
        verbose_name="звезда")
    movie = models.ForeignKey(  # Привязка к фильму которому добавили рейт
        Movie,
        on_delete=models.CASCADE,
        verbose_name="фильм",
        related_name="ratings")

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)

    parent = models.ForeignKey(
        'self',
        verbose_name="Родитель",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    movie = models.ForeignKey(
        Movie,
        verbose_name="фильм",
        on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

