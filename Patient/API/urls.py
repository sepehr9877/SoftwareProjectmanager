from django.urls import path
from .views import GetPateintAppointmentwithDoctor,GetPatientAppointmentwithCounselorApi
urlpatterns=[
    path('patient/counsellor/getallappointment',GetPatientAppointmentwithCounselorApi.as_view()),
    path('patient/doctor/getallappointment',GetPateintAppointmentwithDoctor.as_view()),
   
]

