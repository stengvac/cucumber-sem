from django import template
import datetime

register = template.Library()


@register.filter(name='success')
def convert_success(value):
    if value:
        return 'success'
    return 'danger'


@register.filter(name='date')
def convert_date(date):
    return date.strftime('%d. %m %Y')
