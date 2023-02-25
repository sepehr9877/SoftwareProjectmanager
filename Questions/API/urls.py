from django.urls import path
from .views import SelfAssessmentApi
urlpatterns=[
    path('SelfAssessment',SelfAssessmentApi.as_view())
]