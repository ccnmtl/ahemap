from django.conf import settings

from django.views.generic.base import TemplateView


# returns important setting information for all web pages.
def django_settings(request):
    whitelist = ['RAVEN_CONFIG']
    return {
        'settings': dict([(k, getattr(settings, k, None))
                          for k in whitelist])}


class IndexView(TemplateView):
    template_name = "main/index.html"
