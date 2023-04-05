from django.urls import path
from .views import GetPateintAppointmentwithDoctor,GetPatientAppointmentwithCounselorApi,\
    RejectAppointmentwithDocotrApi,RejectAppointmentwithCounselorApi
urlpatterns=[
    path('patient/counsellor/getallappointment',GetPatientAppointmentwithCounselorApi.as_view()),
    path('patient/doctor/getallappointment',GetPateintAppointmentwithDoctor.as_view()),
    path('patient/reject/appointment/doctor',RejectAppointmentwithDocotrApi.as_view()),
    path('patient/reject/appointment/counselor',RejectAppointmentwithCounselorApi.as_view())

]

