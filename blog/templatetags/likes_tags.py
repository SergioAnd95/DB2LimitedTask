import datetime
from django import template

register = template.Library()

@register.simple_tag
def like_exist(post, user):
    return post.user_like_exist(user)