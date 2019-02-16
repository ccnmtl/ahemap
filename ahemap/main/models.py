from django.contrib.gis.db.models.fields import PointField
from django.db import models


ACCREDITATION_CHOICES = (
        ('R', 'Regional'),
        ('N', 'National'),
    )


class Institution(models.Model):
    external_id = models.PositiveIntegerField(unique=True)
    title = models.TextField(unique=True)
    latlng = PointField()

    address = models.TextField(null=True, blank=True)
    city = models.TextField()
    state = models.CharField(max_length=2)

    admin_name = models.TextField()
    admin_email = models.EmailField()
    admin_phone = models.TextField()

    website_url = models.URLField()
    image = models.URLField(null=True, blank=True)
    admissions_url = models.URLField(null=True, blank=True)

    private = models.BooleanField()

    student_population = models.PositiveIntegerField()
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
    jst_credits_accepted = models.BooleanField()
    dsst_credits_accepted = models.BooleanField()
    online_credits_accepted = models.BooleanField()
    application_fee_waived = models.BooleanField()

    vet_grants_scholarships = models.BooleanField()
    vet_grants_scholarships_notes = models.TextField(null=True, blank=True)

    yellow_ribbon = models.BooleanField()
    yellow_ribbon_slots = models.PositiveIntegerField(null=True)
    yellow_ribbon_contribution = models.PositiveIntegerField(null=True)

    notes = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
