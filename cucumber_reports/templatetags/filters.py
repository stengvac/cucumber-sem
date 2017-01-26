from django import template

register = template.Library()


@register.filter(name='success')
def convert_success(value):
    if value:
        return 'success'
    return 'danger'
