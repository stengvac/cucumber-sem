from django import template
import datetime

register = template.Library()


@register.filter(name='success')
def convert_success(value):
    """
    Convert boolean values to css representation

    :param value: to convert
    :return: 'success' for ture and 'danger' for false
    """
    if value:
        return 'success'
    return 'danger'


@register.filter(name='date')
def convert_date(date):
    """
    Convert datetime object to string

    :param date: to convert
    :return: string representation of date
    """
    return date.strftime('%d. %m. %Y')


@register.filter(name='duration')
def convert_millis_to_time(millis):
    """
    Convert given millis to human readable format

    :param millis duration of step run
    :return: seconds and microseconds as string
    """
    delta = datetime.timedelta(milliseconds=millis)

    return '{}.{}'.format(delta.seconds, delta.microseconds)
