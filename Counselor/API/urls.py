from django.urls import path
from .views import CounselorAllPatient,CounselorMangeDoctorApi,ListofDoctorsAi,\
    CounselorPatientAppointmentApi
urlpatterns=[
    path('counselor/addappointment/patient',CounselorAllPatient.as_view()),
    path('counselor/listofdoctors',ListofDoctorsAi.as_view()),
    path('counselor/manage/patientdoctor',CounselorMangeDoctorApi.as_view()),
    path('counselor/details/bydate',CounselorPatientAppointmentApi.as_view()),

]