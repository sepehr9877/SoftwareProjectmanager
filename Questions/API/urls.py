from django.urls import path
from .views import SelfAssessmentApi,GetAllSelfAssessmentApi
urlpatterns=[
    path('patient/selfassessment',SelfAssessmentApi.as_view()),
    path('getallselfassessment',GetAllSelfAssessmentApi.as_view())
]