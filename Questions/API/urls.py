from django.urls import path
from .views import SelfAssessmentApi
urlpatterns=[
    path('selfassessment',SelfAssessmentApi.as_view())
]