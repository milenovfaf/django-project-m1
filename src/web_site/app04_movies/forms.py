# from django.forms import ModelForm, TextInput
from django import forms
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from .models import Reviews, RatingStar, Rating

'''Проверка валидации с помощью встроенной в джанго функциональностью,
Джанго заполнит эту форму вьюхе таким образом CommentForm(request.POST) '''
# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ('author_name', 'email', 'text')


class ReviewsForm(forms.ModelForm):
    """ Форма отзывов """
    captcha = ReCaptchaField()  # Добавим поле капча и в Meta>fields отобразим

    class Meta:
        model = Reviews
        fields = ('name', 'email', 'text', 'captcha')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control border'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control border'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control border'
            }),

        }

        # Добавление атрибутов к полям, например плейсхолдер и класс как в html
    #     widgets = {
    #         'title': forms.TextInput(attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Название статьи'
    #         }),
    #         'anons': forms.TextInput(attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Анонс статьи'
    #         }),
    #         'date': forms.DateTimeInput(attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Дата публикации'
    #         }),
    #         'full_text': forms.Textarea(attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Текст статьи'
    #         })
    #     }
    # #


class RatingForm(forms.ModelForm):
    """ Форма добавления рейтинга """
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(),  # Получаем все звёзды
        widget=forms.RadioSelect(),   # Виджет формы (внешний вид)
        empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star",)
        """ Чтобы выводить список добавленных звёзд, нужно переопределить 
        поле star, с помощью ModelChoiceField"""
