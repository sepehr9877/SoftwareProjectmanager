from django.urls import path
from .views import DoctorPatientApi,DoctorCreateNewAppointmentApi,DoctorGetAppointmentApi
urlpatterns=[
    path('doctor/manage/patient',DoctorPatientApi.as_view()),
    path('doctor/create/newappointment',DoctorCreateNewAppointmentApi.as_view()),
    path('doctor/details/bydate',DoctorGetAppointmentApi.as_view())
]