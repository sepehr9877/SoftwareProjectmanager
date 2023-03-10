from django.urls import path
from .views import CounselorAllPatient,CounselorMangeDoctorApi,ListofDoctorsAi
urlpatterns=[
    path('counselor/addappointment/patient',CounselorAllPatient.as_view()),
    path('counselor/listofdoctors',ListofDoctorsAi.as_view()),
    path('counselor/manage/patientdoctor',CounselorMangeDoctorApi.as_view()),
]