from django.urls import path
from .views import CounselorPatientApi,SetAppointment
urlpatterns=[
    path('CounselorPatients',CounselorPatientApi.as_view()),
    path('SetAppointment',SetAppointment.as_view())
]