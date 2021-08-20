from django import template
from django.urls import reverse
import re
register = template.Library()


@register.filter(name='hide_email')
def hide_email(value):
    hide = value[2:value.find("@")]
    return str(value.replace(hide, "*"*(4 if len(hide)>4 else len(hide))))

@register.filter(name='absolute_path')
def absolute_path(path):
    if path == reverse('register') or path == reverse('login'):
        return 'true'
    elif path == reverse('reset_password'):
        return 'pReset'
    elif path == reverse('password_reset_done'):
        return 'pSent'
    return 3

@register.filter(name='addInputClass')
def addInputClass(value, placeholder):
    print(str(value))
    return str(' '.join([str(value)[:-1], f'class="form-control" placeholder={placeholder}>']))
