from django.urls import path
from .views import CounselorPatientApi
urlpatterns=[
    path('CounselorPatients',CounselorPatientApi.as_view())
]