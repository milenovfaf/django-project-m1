from django import template
from app05_contact.forms import ContactForm

register = template.Library()


@register.inclusion_tag('contact/tags/form.html')
def contact_form():
    return {'contact_form': ContactForm()}

""" Создаём темплейт тэг, который будет возвращать форму которую мы будем
подпихивать в футер на каждой странице {% load contact_tags %} """
