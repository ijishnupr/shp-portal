from django.db import models
from django.contrib.auth.models import User

class Survey(models.Model):
    # --- STATUS CHOICES ---
    STATUS_CHOICES = [
        ('Proposed', 'Proposed'),
        ('Under Construction', 'Under Construction'),
        ('Operational', 'Operational'),
    ]
    
    SITE_TYPE_CHOICES = [
        ('River', 'River'),
        ('Canal', 'Canal'),
        ('Dam Toe', 'Dam Toe'),
    ]

    # --- Section 1: Site Information ---
    site_name = models.CharField(max_length=200)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    river_stream_name = models.CharField(max_length=200)
    site_type = models.CharField(max_length=50, choices=SITE_TYPE_CHOICES)

    # --- Section 2: Hydrological Data ---
    installed_capacity_mw = models.DecimalField(max_digits=10, decimal_places=2, help_text="In MW")
    type_of_turbine = models.CharField(max_length=100)
    avg_annual_rainfall_mm = models.FloatField(help_text="In mm")
    avg_discharge = models.FloatField(help_text="m3/s")

    # --- Section 3: Technical Data ---
    generator_capacity_mw = models.DecimalField(max_digits=10, decimal_places=2, help_text="In MW")
    annual_energy_production = models.FloatField(help_text="Units in MU or kWh")

    # --- Section 4: Status and Classification ---
    current_status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    is_rejected = models.BooleanField(default=False)
    reason_for_rejection = models.TextField(blank=True, null=True)

    # --- Section 5: Documents (Files) ---
    # These store the file in S3/Local and the Path in MySQL
    fr_report = models.FileField(upload_to='fr_reports/', blank=True, null=True, verbose_name="Feasibility Report (FR)")
    special_study_report = models.FileField(upload_to='special_studies/', blank=True, null=True)
    env_clearance_doc = models.FileField(upload_to='env_docs/', blank=True, null=True, verbose_name="Environmental Clearance")

    # --- Meta ---
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.site_name} - {self.district}"