from django import template


register = template.Library()


# https://stackoverflow.com/questions/2295725/extending-urlize-in-django
@register.filter(is_safe=True)
def url_target_blank(text):
    return text.replace('<a ', '<a target="_blank" ')
