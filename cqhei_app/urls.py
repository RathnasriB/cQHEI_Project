from django.urls import path
from . import views

urlpatterns = [
    path('', views.survey_form, name='survey_form'),
    path('success/<int:survey_id>/', views.survey_success, name='survey_success'),
    # path('results/', views.survey_results, name='survey_results'),  # Remove this for now
]