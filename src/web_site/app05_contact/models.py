from django.db import models


class Contact(models.Model):
    """ Подписка по email """
    # Поле автоматически заполняется при создании записи
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)
    # editable=True

    def __str__(self):
        return self.email
