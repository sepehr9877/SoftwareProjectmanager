from django.urls import path
from .views import AcceptRejectDoctorApi,\
    AcceptRejectCounselorApi,\
    ManagerGetPatientOfDoctorByDate,\
    ManagerGetPatientofCounselorByDate,MangerAcceptRejectPatients
urlpatterns=[
    path('manager/accept_reject/doctor',AcceptRejectDoctorApi.as_view()),
    path('manager/accept_reject/counselor',AcceptRejectCounselorApi.as_view()),
    path('manger/accept_reject/patient',MangerAcceptRejectPatients.as_view()),
    path('manager/getpatients/doctor/bydate',ManagerGetPatientOfDoctorByDate.as_view()),
    path('manager/getpatients/counselor/bydate',ManagerGetPatientofCounselorByDate.as_view())
]