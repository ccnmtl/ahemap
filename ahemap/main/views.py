from django.conf import settings
from django.utils.html import escape
from django.views.generic.base import TemplateView
from rest_framework import viewsets

from ahemap.main.models import Institution
from ahemap.main.serializers import InstitutionSerializer


# returns important setting information for all web pages.
def django_settings(request):
    whitelist = ['RAVEN_CONFIG']
    return {
        'settings': dict([(k, getattr(settings, k, None))
                          for k in whitelist])}


class IndexView(TemplateView):
    template_name = "main/index.html"


class MapView(TemplateView):
    template_name = "main/map.html"


class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer

    def filter(self, qs):
        # filter by a search term
        q = self.request.GET.get('q', None)
        if q:
            qs = qs.filter(title__contains=escape(q))

        return qs

    def get_queryset(self):
        qs = Institution.objects.all()
        return self.filter(qs)
