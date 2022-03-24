from django.contrib.gis.db.models.fields import PointField
from django.contrib.gis.geos.point import Point
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.db.models.fields import BooleanField, PositiveIntegerField


ACCREDITATION_CHOICES = (
    ('R', 'regional'),
    ('N', 'national'),
)


class InstitutionManager(models.Manager):

    FIELD_MAPPING = [
        'external_id',
        '',
        '',
        '',
        'title',
        'website_url',
        'student_population',
        'set_institution_type',
        'set_program_duration',
        'image',
        'address',
        'city',
        'state',
        'set_latitude',
        'set_longitude',
        'undergrad_vet_population',
        'undergrad_vet_graduation_rate',
        'grad_vet_population',
        'grad_vet_graduation_rate',
        'admissions_url',
        'vet_center',
        'sva_chapter',
        'standardized_test_required',
        'standardized_test_notes',
        'notes',
        'accredited',
        'set_accreditation_type',
        'regional_accreditor',
        'clep_credits_accepted',
        'jst_credits_accepted',
        'dsst_credits_accepted',
        'yellow_ribbon',
        'yellow_ribbon_slots',
        'yellow_ribbon_contribution',
        'online_credits_accepted',
        'application_fee_waived',
        'vet_grants_scholarships',
        'vet_grants_scholarships_notes',
        'undergraduate_population'
    ]

    def find_or_create_by_external_id(self, external_id):
        try:
            inst = Institution.objects.get(external_id=external_id)
        except Institution.DoesNotExist:
            inst = Institution(external_id=external_id)

        return inst

    def _set_field_value(self, inst, field_name, value):
        try:
            field = Institution._meta.get_field(field_name)

            if not value:
                setattr(inst, field.name, None)
            elif isinstance(field, BooleanField):
                setattr(inst, field.name, 'yes' in value.lower())
            elif isinstance(field, PositiveIntegerField):
                try:
                    value = value.replace(',', '')
                    setattr(inst, field.name, int(value))
                except ValueError:
                    pass
            else:
                setattr(inst, field.name, value)
        except FieldDoesNotExist:
            # if the field doesn't exist, the attribute should be callable
            getattr(inst, field_name, None)(value)

    def update_or_create(self, row):
        external_id_idx = 0
        inst = self.find_or_create_by_external_id(int(row[external_id_idx]))
        for idx, value in enumerate(row[1:]):
            field_name = self.FIELD_MAPPING[idx + 1]
            if field_name:
                self._set_field_value(inst, field_name, value.strip())
        inst.save()
        return inst


class Institution(models.Model):
    objects = InstitutionManager()

    external_id = models.PositiveIntegerField()
    title = models.TextField()
    latlng = PointField()

    address = models.TextField(null=True, blank=True)
    city = models.TextField()
    state = models.CharField(max_length=2)

    website_url = models.URLField()
    image = models.URLField(null=True, blank=True)
    admissions_url = models.URLField(null=True, blank=True)

    private = models.BooleanField()

    student_population = models.PositiveIntegerField()
    undergraduate_population = models.PositiveIntegerField()

    undergrad_vet_population = models.PositiveIntegerField(null=True)
    undergrad_vet_graduation_rate = models.PositiveIntegerField(null=True)
    grad_vet_population = models.PositiveIntegerField(null=True)
    grad_vet_graduation_rate = models.PositiveIntegerField(null=True)

    two_year_program = models.BooleanField(null=True)
    four_year_program = models.BooleanField(null=True)

    accredited = models.BooleanField()
    accreditation_type = models.CharField(
        null=True, max_length=1, choices=ACCREDITATION_CHOICES)
    regional_accreditor = models.TextField(null=True, blank=True)

    standardized_test_required = models.BooleanField()
    standardized_test_notes = models.TextField(null=True, blank=True)

    vet_center = models.BooleanField()
    sva_chapter = models.BooleanField()

    clep_credits_accepted = models.BooleanField()
    jst_credits_accepted = models.BooleanField(null=True, blank=True)
    dsst_credits_accepted = models.BooleanField()
    online_credits_accepted = models.BooleanField()
    application_fee_waived = models.BooleanField()

    vet_grants_scholarships = models.BooleanField()
    vet_grants_scholarships_notes = models.TextField(null=True, blank=True)

    yellow_ribbon = models.BooleanField()
    yellow_ribbon_slots = models.TextField(null=True, blank=True)
    yellow_ribbon_contribution = models.TextField(null=True, blank=True)

    notes = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def set_accreditation_type(self, value):
        self.accreditation_type = None

        value = value.lower()
        for s in ACCREDITATION_CHOICES:
            if value == s[1]:
                self.accreditation_type = s[0]

    def get_institution_type(self):
        return 'Private' if self.private else 'Public'

    def set_institution_type(self, value):
        self.private = 'private' in value.lower()

    def set_program_duration(self, value):
        value = value.lower()
        self.two_year_program = '2 year' in value
        self.four_year_program = '4 year' in value

    def set_latitude(self, value):
        if not self.latlng:
            self.latlng = Point(float(value), 0)
        else:
            self.latlng = Point(float(value), self.latlng.coords[1])

    def set_longitude(self, value):
        if not self.latlng:
            self.latlng = Point(0, float(value))
        else:
            self.latlng = Point(self.latlng.coords[0], float(value))
