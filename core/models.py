from django.db import models
from django.contrib.auth.models import User

class Survey(models.Model):
    # --- CHOICES ---
    ACCESS_CHOICES = [('Road', 'Road'), ('Footpath', 'Footpath'), ('River Crossing', 'River Crossing')]
    FLOW_TYPE_CHOICES = [('Perennial', 'Perennial'), ('Seasonal', 'Seasonal')]
    FLOW_COND_CHOICES = [('Lean', 'Lean'), ('Average', 'Average'), ('Flood', 'Flood')]
    MEASURE_METHOD = [('Float', 'Float'), ('Bucket', 'Bucket'), ('Visual Estimate', 'Visual Estimate')]
    OWNERSHIP_CHOICES = [('Forest', 'Forest'), ('Private', 'Private'), ('Estate', 'Estate'), ('Temple', 'Temple'), ('Govt', 'Govt')]
    VOLTAGE_CHOICES = [('LT', 'LT'), ('11kV', '11kV'), ('33kV', '33kV')]
    ESTIMATE_BASIS = [('Thumb rule', 'Thumb rule'), ('PMT guidance', 'PMT guidance')]
    CONFIDENCE_LEVEL = [('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')]
    FEASIBILITY_CHOICES = [('Promising', 'Promising'), ('Uncertain', 'Uncertain'), ('Not promising', 'Not promising')]
    MONTH_CHOICES = [
        ('Jan', 'Jan'), ('Feb', 'Feb'), ('Mar', 'Mar'), ('Apr', 'Apr'), ('May', 'May'), ('Jun', 'Jun'),
        ('Jul', 'Jul'), ('Aug', 'Aug'), ('Sep', 'Sep'), ('Oct', 'Oct'), ('Nov', 'Nov'), ('Dec', 'Dec')
    ]

    # --- SECTION 0: ADMINISTRATIVE METADATA ---
    survey_date = models.DateTimeField(auto_now_add=True)
    student_team_id = models.CharField(max_length=50, verbose_name="Student Team ID")
    pmt_name = models.CharField(max_length=100, verbose_name="PMT Name") # Can be a dropdown in form
    district = models.CharField(max_length=100)
    river_basin = models.CharField(max_length=100)

    # --- SECTION 1: SITE IDENTIFICATION ---
    proposed_site_code = models.CharField(max_length=50, blank=True, help_text="EMC Format")
    local_site_name = models.CharField(max_length=200, blank=True)
    stream_name = models.CharField(max_length=200)
    village_panchayat = models.CharField(max_length=200, verbose_name="Village / Panchayat")
    nearest_landmark = models.CharField(max_length=200, blank=True)

    # --- SECTION 2: LOCATION (GPS) ---
    # Intake
    intake_latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Intake Lat")
    intake_longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Intake Long")
    intake_elevation_m = models.FloatField(verbose_name="Intake Elevation (m)")
    # Powerhouse
    powerhouse_latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="PH Lat")
    powerhouse_longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="PH Long")
    powerhouse_elevation_m = models.FloatField(blank=True, null=True, verbose_name="PH Elevation (m)")

    # --- SECTION 3: ACCESS & SITE CONDITIONS ---
    access_type = models.CharField(max_length=50, choices=ACCESS_CHOICES)
    distance_from_road_km = models.FloatField(verbose_name="Distance from road (km)")
    seasonal_access_constraints = models.TextField(blank=True, help_text="Monsoon / landslide / forest restriction")

    # --- SECTION 4: STREAM & FLOW ---
    flow_type = models.CharField(max_length=50, choices=FLOW_TYPE_CHOICES)
    qualitative_flow_desc = models.TextField(verbose_name="Qualitative Flow Description")
    observed_flow_condition = models.CharField(max_length=50, choices=FLOW_COND_CHOICES)
    diversions_upstream = models.BooleanField(default=False, verbose_name="Any Diversions Upstream?")

    # --- SECTION 5: HEAD & DISCHARGE ---
    measured_head_m = models.FloatField(verbose_name="Measured Head (m)")
    dem_assisted_head_m = models.FloatField(blank=True, null=True, verbose_name="DEM-assisted Head (m)")
    
    discharge_measured = models.BooleanField(default=False, verbose_name="Discharge Measurement Taken?")
    measured_discharge_lps = models.FloatField(blank=True, null=True, verbose_name="Measured Discharge (lps)")
    measurement_method = models.CharField(max_length=50, choices=MEASURE_METHOD, blank=True)
    season_of_measurement = models.CharField(max_length=20, choices=MONTH_CHOICES, blank=True)

    # --- SECTION 6: LAND OWNERSHIP ---
    land_ownership = models.CharField(max_length=50, choices=OWNERSHIP_CHOICES)
    forest_boundary_within_500m = models.BooleanField(default=False)
    known_clearances_needed = models.TextField(blank=True)

    # --- SECTION 7: ENV & SOCIAL ---
    nearby_wildlife = models.BooleanField(default=False, verbose_name="Nearby Wildlife Presence")
    waterfall_within_500m = models.BooleanField(default=False)
    tribal_settlement_nearby = models.BooleanField(default=False)
    # Stored as comma-separated string for simplicity
    existing_water_uses = models.CharField(max_length=255, help_text="Irrigation, Drinking, Tourism, etc.") 
    social_sensitivities = models.TextField(blank=True)

    # --- SECTION 8: GRID CONNECTIVITY ---
    nearest_kseb_line_km = models.FloatField(verbose_name="Nearest KSEB Line Distance (km)")
    voltage_level = models.CharField(max_length=20, choices=VOLTAGE_CHOICES)
    nearest_substation = models.CharField(max_length=100)

    # --- SECTION 9: POWER POTENTIAL ---
    indicative_capacity_kw = models.FloatField(verbose_name="Indicative Installed Capacity (kW)")
    basis_of_estimate = models.CharField(max_length=50, choices=ESTIMATE_BASIS)
    tentative_plf = models.FloatField(blank=True, null=True, verbose_name="Tentative PLF")

    # --- SECTION 10: HYDROLOGY CORRELATION ---
    nearby_gauge_station = models.CharField(max_length=100, blank=True, verbose_name="Nearby CWC/KSEB Gauge")
    correlation_method = models.CharField(max_length=50, choices=[('Area ratio', 'Area ratio'), ('Regional', 'Regional')])
    confidence_level = models.CharField(max_length=20, choices=CONFIDENCE_LEVEL)

    # --- SECTION 11: PHOTOS (Geo-tagged) ---
    photo_intake = models.ImageField(upload_to='photos/intake/', verbose_name="Intake Location Photo")
    photo_powerhouse = models.ImageField(upload_to='photos/powerhouse/', verbose_name="Powerhouse Location Photo")
    photo_upstream = models.ImageField(upload_to='photos/upstream/', verbose_name="Stream Upstream Photo")
    photo_access = models.ImageField(upload_to='photos/access/', verbose_name="Access Route Photo")

    # --- SECTION 12: ASSESSMENT ---
    overall_feasibility = models.CharField(max_length=50, choices=FEASIBILITY_CHOICES)
    key_constraints = models.TextField()
    recommend_tier_1 = models.BooleanField(default=False, verbose_name="Recommend for Tier-1 Study")

    # Metadata
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.student_team_id} - {self.stream_name}"