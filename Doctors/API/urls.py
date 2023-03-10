from django.urls import path
from .views import DoctorPatientApi,DoctorCreateNewAppointmentApi
urlpatterns=[
    path('doctor/manage/patient',DoctorPatientApi.as_view()),
    path('doctor/create/newappointment',DoctorCreateNewAppointmentApi.as_view())
]