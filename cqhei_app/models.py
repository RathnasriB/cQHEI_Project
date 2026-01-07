from django.db import models
from django.core.exceptions import ValidationError


class CQHEISurvey(models.Model):
    # ================= BASIC INFORMATION =================
    survey_date = models.DateField(verbose_name="Date")
    river_code = models.CharField(max_length=50, verbose_name="River Code")
    river_mile = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="River Mile")
    clarity = models.CharField(max_length=100, verbose_name="Clarity", blank=True)
    forest_ule_number = models.CharField(max_length=50, verbose_name="Forest/Ule Number", blank=True)
    cluster_number = models.CharField(max_length=50, verbose_name="Cluster Number", blank=True)
    river_site = models.CharField(max_length=200, verbose_name="River Site")
    name_group = models.CharField(max_length=200, verbose_name="Name/Group")

    # ================= REACH INFORMATION =================
    REACH_LENGTH_CHOICES = [
        ('50m', '50m'),
        ('100m', '100m'),
        ('150m', '150m'),
        ('200m', '200m'),
        ('500m', '500m'),
        ('750m', '750m'),
        ('other', 'Other'),
    ]
    reach_length = models.CharField(max_length=20, choices=REACH_LENGTH_CHOICES)
    reach_length_custom = models.CharField(max_length=100, blank=True)

    # ================= SECTION I =================
    substrate_mostly_large = models.BooleanField(default=False)
    substrate_mostly_medium = models.BooleanField(default=False)
    substrate_mostly_small = models.BooleanField(default=False)
    substrate_dominated_bedrock = models.BooleanField(default=False)
    substrate_mostly_very_fine = models.BooleanField(default=False)

    smothering_no = models.BooleanField(default=False)
    smothering_yes = models.BooleanField(default=False)

    silting_no = models.BooleanField(default=False)
    silting_yes = models.BooleanField(default=False)

    # ================= SECTION II (form-only fields) =================
    cover_underwater_tree_roots_large = models.BooleanField(default=False)
    cover_underwater_tree_rootlets = models.BooleanField(default=False)
    cover_boulders = models.BooleanField(default=False)
    cover_backwaters = models.BooleanField(default=False)
    cover_downed_trees = models.BooleanField(default=False)
    cover_deep_areas = models.BooleanField(default=False)
    cover_undercut_banks = models.BooleanField(default=False)
    cover_water_plants = models.BooleanField(default=False)
    cover_shallow_slow_areas = models.BooleanField(default=False)
    cover_shrubs_small_trees = models.BooleanField(default=False)

    # ================= SECTION III =================
    curviness_two_plus_good_bends = models.BooleanField(default=False)
    curviness_one_two_good_bends = models.BooleanField(default=False)
    curviness_mostly_straight = models.BooleanField(default=False)
    curviness_very_straight = models.BooleanField(default=False)

    natural_mostly_natural = models.BooleanField(default=False)
    natural_minor_changes = models.BooleanField(default=False)
    natural_many_changes = models.BooleanField(default=False)
    natural_heavy_changes = models.BooleanField(default=False)

    # ================= SECTION IV =================
    width_wide = models.BooleanField(default=False)
    width_narrow = models.BooleanField(default=False)
    width_none = models.BooleanField(default=False)

    landuse_forest_wetland = models.BooleanField(default=False)
    landuse_shrubs = models.BooleanField(default=False)
    landuse_overgrown_fields = models.BooleanField(default=False)
    landuse_fenced_pasture = models.BooleanField(default=False)
    landuse_park = models.BooleanField(default=False)
    landuse_conservation_tillage = models.BooleanField(default=False)

    erosion_urban_industrial = models.BooleanField(default=False)
    erosion_open_pasture = models.BooleanField(default=False)
    erosion_suburban_rowcrop = models.BooleanField(default=False)
    erosion_raw_collapsing = models.BooleanField(default=False)

    shading_mostly = models.BooleanField(default=False)
    shading_partly = models.BooleanField(default=False)
    shading_none = models.BooleanField(default=False)

    # ================= SECTION V =================
    depth_chest_deep = models.BooleanField(default=False)
    depth_waist_deep = models.BooleanField(default=False)
    depth_knee_deep = models.BooleanField(default=False)
    depth_ankle_deep = models.BooleanField(default=False)

    flow_very_fast = models.BooleanField(default=False)
    flow_fast = models.BooleanField(default=False)
    flow_moderate = models.BooleanField(default=False)
    flow_slow = models.BooleanField(default=False)
    flow_none = models.BooleanField(default=False)

    # ================= SECTION VI =================
    riffles_knee_deep_fast = models.BooleanField(default=False)
    riffles_ankle_calf_fast = models.BooleanField(default=False)
    riffles_ankle_shallow_slow = models.BooleanField(default=False)
    riffles_none = models.BooleanField(default=False)

    substrate_fist_size = models.BooleanField(default=False)
    substrate_smaller_fist = models.BooleanField(default=False)
    substrate_smaller_fingernail = models.BooleanField(default=False)

    # ==================================================
    # ✅ MODEL-LEVEL VALIDATION FOR "OTHER"
    # ==================================================
    def clean(self):
        if self.reach_length == "other" and not self.reach_length_custom:
            raise ValidationError({
                "reach_length_custom": "Please specify the reach length when 'Other' is selected."
            })

        if self.reach_length != "other":
            self.reach_length_custom = ""

    def __str__(self):
        return f"CQHEI Survey - {self.river_site} ({self.survey_date})"


# =====================================================
# SECTION II BACKEND TABLE (EXISTING SQL TABLE)
# =====================================================

class Cover(models.Model):
    cover_id = models.AutoField(primary_key=True, db_column='Cover_ID')

    cqhei_new_x_id = models.IntegerField(db_column='cQHEI_New_X_ID')

    underwater_tree_roots = models.IntegerField(db_column='Underwater_Tree_Roots', default=0)
    underwater_tree_rootlets = models.IntegerField(db_column='Underwater_Tree_Rootlets', default=0)
    boulders = models.IntegerField(db_column='Boulders', default=0)
    oxbows_backwaters = models.IntegerField(db_column='Oxbows_Backwaters', default=0)
    downed_trees = models.IntegerField(db_column='Downed_trees', default=0)
    shallows = models.IntegerField(db_column='Shallows', default=0)
    water_plants = models.IntegerField(db_column='Water_Plants', default=0)
    deep_pools = models.IntegerField(db_column='Deep_Pools', default=0)
    overhanging_vegetation = models.IntegerField(db_column='Overhanging_Vegetation', default=0)
    undercut_banks = models.IntegerField(db_column='Undercut_Banks', default=0)

    cover_score = models.IntegerField(db_column='Cover_Score', null=True, blank=True)

    created_timestamp = models.DateTimeField(db_column='Created_Timestamp', auto_now_add=True)
    last_updated_timestamp = models.DateTimeField(db_column='Last_Updated_Timestamp', auto_now=True)

    class Meta:
        db_table = 'cQHEI.Cover'
        managed = False
