from django import forms
from .models import CQHEISurvey


class CQHEISurveyForm(forms.ModelForm):
    class Meta:
        model = CQHEISurvey
        fields = '__all__'
        widgets = {
            # Basic Information
            'survey_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'river_code': forms.TextInput(attrs={'class': 'form-control'}),
            'river_mile': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'clarity': forms.TextInput(attrs={'class': 'form-control'}),
            'forest_ule_number': forms.TextInput(attrs={'class': 'form-control'}),
            'cluster_number': forms.TextInput(attrs={'class': 'form-control'}),
            'river_site': forms.TextInput(attrs={'class': 'form-control'}),
            'name_group': forms.TextInput(attrs={'class': 'form-control'}),
            'reach_length': forms.Select(attrs={'class': 'form-select'}),
            'reach_length_custom': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Required fields
        self.fields['survey_date'].required = True
        self.fields['river_code'].required = True
        self.fields['river_mile'].required = True
        self.fields['river_site'].required = True
        self.fields['name_group'].required = True
        self.fields['reach_length'].required = True

        # IMPORTANT: custom length should NOT be required by default
        self.fields['reach_length_custom'].required = False

    def clean(self):
        cleaned_data = super().clean()

        # ===============================
        # SINGLE-CHOICE SECTION VALIDATION
        # ===============================
        single_choice_sections = [
            {
                'fields': [
                    'substrate_mostly_large', 'substrate_mostly_medium',
                    'substrate_mostly_small', 'substrate_dominated_bedrock',
                    'substrate_mostly_very_fine'
                ],
                'error': "Please select only one option for Substrate Size in Section I."
            },
            {
                'fields': ['smothering_yes', 'smothering_no'],
                'error': "Please select only one option for Smothering in Section I."
            },
            {
                'fields': ['silting_yes', 'silting_no'],
                'error': "Please select only one option for Silting in Section I."
            },
            {
                'fields': [
                    'curviness_two_plus_good_bends', 'curviness_one_two_good_bends',
                    'curviness_mostly_straight', 'curviness_very_straight'
                ],
                'error': "Please select only one option for Curviness in Section III."
            },
            {
                'fields': [
                    'natural_mostly_natural', 'natural_minor_changes',
                    'natural_many_changes', 'natural_heavy_changes'
                ],
                'error': "Please select only one option for Natural Condition in Section III."
            },
            {
                'fields': ['width_wide', 'width_narrow', 'width_none'],
                'error': "Please select only one option for Width in Section IV."
            },
            {
                'fields': [
                    'landuse_forest_wetland', 'landuse_shrubs',
                    'landuse_overgrown_fields', 'landuse_fenced_pasture',
                    'landuse_park', 'landuse_conservation_tillage'
                ],
                'error': "Please select only one option for Land Use in Section IV."
            },
            {
                'fields': [
                    'erosion_urban_industrial', 'erosion_open_pasture',
                    'erosion_suburban_rowcrop', 'erosion_raw_collapsing'
                ],
                'error': "Please select only one option for Erosion in Section IV."
            },
            {
                'fields': ['shading_mostly', 'shading_partly', 'shading_none'],
                'error': "Please select only one option for Shading in Section IV."
            },
            {
                'fields': [
                    'depth_chest_deep', 'depth_waist_deep',
                    'depth_knee_deep', 'depth_ankle_deep'
                ],
                'error': "Please select only one option for Depth in Section V."
            },
            {
                'fields': [
                    'riffles_knee_deep_fast', 'riffles_ankle_calf_fast',
                    'riffles_ankle_shallow_slow', 'riffles_none'
                ],
                'error': "Please select only one option for Riffles in Section VI."
            },
            {
                'fields': [
                    'substrate_fist_size', 'substrate_smaller_fist',
                    'substrate_smaller_fingernail'
                ],
                'error': "Please select only one option for Substrate in Section VI."
            },
        ]

        for section in single_choice_sections:
            selected = sum(1 for field in section['fields'] if cleaned_data.get(field))
            if selected > 1:
                raise forms.ValidationError(section['error'])

        # ===============================
        # FIX: Reach Length "Other"
        # ===============================
        reach_length = cleaned_data.get('reach_length')
        reach_length_custom = cleaned_data.get('reach_length_custom')

        # IMPORTANT FIX:
        # compare case-insensitive + string safe
        if reach_length and str(reach_length).lower() == 'other':
            if not reach_length_custom:
                self.add_error(
                    'reach_length_custom',
                    "Please specify the exact length when selecting 'Other'."
                )

        return cleaned_data

    def clean_river_mile(self):
        river_mile = self.cleaned_data.get('river_mile')
        if river_mile is not None:
            if river_mile < 0:
                raise forms.ValidationError("River mile cannot be negative.")
            if river_mile > 999.99:
                raise forms.ValidationError("River mile cannot exceed 999.99.")
        return river_mile

    def clean_survey_date(self):
        survey_date = self.cleaned_data.get('survey_date')
        if survey_date:
            from django.utils import timezone
            if survey_date > timezone.now().date():
                raise forms.ValidationError("Survey date cannot be in the future.")
        return survey_date
