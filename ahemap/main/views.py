import csv
from urllib.parse import urlencode

from ahemap.main.forms import InstitutionImportForm
from ahemap.main.models import Institution
from ahemap.main.serializers import InstitutionSerializer
from ahemap.main.utils import sanitize, validate_state
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.http.response import StreamingHttpResponse
from django.urls.base import reverse
from django.utils.functional import cached_property
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from rest_framework import viewsets


# returns important setting information for all web pages.
def django_settings(request):
    whitelist = [
        'RAVEN_CONFIG', 'SENTRY_DSN',
        'GOOGLE_MAP_API', 'JIRA_CONFIGURATION'
    ]
    return {
        'settings': dict([(k, getattr(settings, k, None))
                          for k in whitelist])}


class HomeView(TemplateView):
    template_name = "main/home.html"
    http_method_names = ['get']


class InstitutionDetailView(DetailView):
    model = Institution
    http_method_names = ['get']


class MapView(TemplateView):
    template_name = "main/map.html"
    http_method_names = ['get']


class InstitutionImportView(FormView):
    template_name = "main/institution_import.html"
    form_class = InstitutionImportForm
    total = 0
    http_method_names = ['get', 'post']

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
            if row[0] == '44':
                print(row)
            Institution.objects.update_or_create(row)
            self.total += 1

        return super(InstitutionImportView, self).form_valid(form)


class InstitutionSearchMixin(object):

    def filter_by_yellow_ribbon(self, qs, params):
        yellow_ribbon = params.get('yellowribbon', 'false') in ['true', 'on']
        if yellow_ribbon:
            return qs.filter(yellow_ribbon=True)
        return qs

    def filter_by_duration(self, qs, params):
        two = params.get('twoyear', 'false') == 'true'
        four = params.get('fouryear', 'false') == 'true'

        if two and not four:
            qs = qs.filter(two_year_program=True)
        elif not two and four:
            qs = qs.filter(four_year_program=True)

        return qs

    def filter_by_public_private(self, qs, params):
        public = params.get('public', None) == 'true'
        private = params.get('private', None) == 'true'

        if public != private:
            return qs.filter(private=private)
        else:
            return qs

    def filter_by_population(self, qs, params):
        pop = params.get('population', None)
        if pop == 'small':
            qs = qs.filter(undergraduate_population__lt=2000)
        elif pop == 'medium':
            qs = qs.filter(
                undergraduate_population__gte=2000,
                undergraduate_population__lte=10000)
        elif pop == 'large':
            qs = qs.filter(undergraduate_population__gt=10000)

        return qs

    def filter_by_state(self, qs, params):
        q = params.get('state', None)
        q = sanitize(q)
        if q and validate_state(q):
            qs = qs.filter(state=q)
        return qs

    def filter_by_name(self, qs, params):
        # filter by a search term
        q = params.get('q', None)
        q = sanitize(q)
        if q:
            qs = qs.filter(title__icontains=q)

        return qs

    def filter_by_site(self, qs, params):
        site = params.get('siteid', None)
        site = sanitize(site)
        if site:
            qs = qs.filter(id=site)
        return qs

    def _get_params(self):
        if self.request.method == 'POST':
            return self.request.POST
        else:
            return self.request.GET

    def filter(self, qs):
        params = self._get_params()
        qs = self.filter_by_duration(qs, params)
        qs = self.filter_by_public_private(qs, params)
        qs = self.filter_by_population(qs, params)
        qs = self.filter_by_state(qs, params)
        qs = self.filter_by_name(qs, params)
        qs = self.filter_by_site(qs, params)
        qs = self.filter_by_yellow_ribbon(qs, params)
        return qs


class PatchedPaginator(Paginator):

    @cached_property
    def count(self):
        return len(self.object_list)


class BrowseView(InstitutionSearchMixin, ListView):
    model = Institution
    http_method_names = ['get']
    paginate_by = 15
    paginator_class = PatchedPaginator

    def valid_context(self, ctx):
        invalid = ['false', '']
        return {k: v for k, v in ctx.items() if v not in invalid}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BrowseView, self).get_context_data(**kwargs)

        ctx = {
            'query': self.request.GET.get('q', ''),
            'twoyear': self.request.GET.get('twoyear', 'false'),
            'fouryear': self.request.GET.get('fouryear', 'false'),
            'public': self.request.GET.get('public', 'false'),
            'private': self.request.GET.get('private', 'false'),
            'population': self.request.GET.get('population', ''),
            'state': self.request.GET.get('state', ''),
            'yellowribbon': self.request.GET.get('yellowribbon', '')
        }

        context.update(ctx)
        context['base_url'] = u'{}?{}&page='.format(
            reverse('browse-view'), urlencode(self.valid_context(ctx)))

        return context

    def get_queryset(self):
        qs = super(BrowseView, self).get_queryset()
        return self.filter(qs)


class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """
        Write the value by returning it, instead of storing in a buffer.
        """
        return value


class SaveView(InstitutionSearchMixin, View):
    http_method_names = ['get']

    def get_header(self):
        return [
            'Institution', 'Address', 'City', 'State',
            'Website', 'Admissions', 'Institution Type',
            'Student Population', 'Undergraduate Population',
            'Undergraduate Veteran Population',
            'Undergraduate Veteran Graduation Rate',
            'Graduate Veteran Population', 'Graduate Veteran Graduation Rate',
            'Two-Year Program', 'Four-Year Program', 'Accredited',
            'Standardized Test Required', 'Age of Standardized Test',
            'Veterans Center', 'SVA Center', 'CLEP Credits Accepted',
            'DSST Credits Accepted', 'JST Credits Accepted',
            'Online Credits Accepted', 'Application Fee Waived',
            'Veteran Grants & Scholarships',
            'Veteran Grants & Scholarships Notes',
            'Yellow Ribbon School', 'Yellow Ribbon Slots',
            'Yellow Ribbon Contributions', 'Notes']

    def get_row(self, inst):
        return [
            inst.title, inst.address, inst.city, inst.state,
            inst.website_url, inst.admissions_url, inst.get_institution_type(),
            inst.student_population, inst.undergraduate_population,
            inst.undergrad_vet_population, inst.undergrad_vet_graduation_rate,
            inst.grad_vet_population, inst.grad_vet_graduation_rate,
            inst.two_year_program, inst.four_year_program, inst.accredited,
            inst.standardized_test_required, inst.standardized_test_notes,
            inst.vet_center, inst.sva_chapter, inst.clep_credits_accepted,
            inst.dsst_credits_accepted, inst.jst_credits_accepted,
            inst.online_credits_accepted, inst.application_fee_waived,
            inst.vet_grants_scholarships, inst.vet_grants_scholarships_notes,
            inst.yellow_ribbon, inst.yellow_ribbon_slots,
            inst.yellow_ribbon_contribution,
            inst.notes]

    def get_rows(self, queryset):
        yield self.get_header()

        for inst in queryset:
            yield self.get_row(inst)

    def get(self, *args, **kwargs):
        qs = self.filter(Institution.objects.all())

        rows = self.get_rows(qs)
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)

        response = StreamingHttpResponse(
            (writer.writerow(row) for row in rows), status=200,
            content_type="text/csv"
        )
        response['Content-Disposition'] = 'attachment; filename="ahe.csv"'
        response['Cache-Control'] = 'no-cache'
        return response


class InstitutionViewSet(InstitutionSearchMixin, viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    http_method_names = ['get']

    def get_queryset(self):
        qs = Institution.objects.all()
        return self.filter(qs)
