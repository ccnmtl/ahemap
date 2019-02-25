from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.urls.base import reverse
from django.utils.html import escape
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from rest_framework import viewsets

from ahemap.main.forms import InstitutionImportForm
from ahemap.main.models import Institution
from ahemap.main.serializers import InstitutionSerializer


# returns important setting information for all web pages.
def django_settings(request):
    whitelist = ['RAVEN_CONFIG', 'GOOGLE_MAP_API']
    return {
        'settings': dict([(k, getattr(settings, k, None))
                          for k in whitelist])}


class IndexView(TemplateView):
    template_name = "main/index.html"


class MapView(TemplateView):
    template_name = "main/map.html"


class InstitutionImportView(FormView):
    template_name = "main/institution_import.html"
    form_class = InstitutionImportForm
    total = 0

    def get_form_kwargs(self):
        kwargs = super(InstitutionImportView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS,
            '{} institutions imported.'.format(self.total),
            extra_tags='safe'
        )

        return reverse('institution-import-view')

    @transaction.atomic
    def form_valid(self, form):
        self.total = 0
        reader = form.csvfile_reader()
        for (idx, row) in enumerate(reader):
            if idx == 0:
                continue  # skip the header
            Institution.objects.update_or_create(row)
            self.total += 1

        return super(InstitutionImportView, self).form_valid(form)


class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer

    def filter(self, qs):
        # filter by a search term
        q = self.request.GET.get('q', None)
        if q:
            qs = qs.filter(title__icontains=escape(q))

        return qs

    def get_queryset(self):
        qs = Institution.objects.all()
        return self.filter(qs)
