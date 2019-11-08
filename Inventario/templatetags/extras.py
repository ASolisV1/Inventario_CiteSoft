## For check user's group
from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='tiene_grupo')
def tiene_grupo(user, group_name):
    return user.groups.filter(name=group_name).exists()