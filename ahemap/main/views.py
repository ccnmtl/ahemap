from django.conf import settings
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


class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
