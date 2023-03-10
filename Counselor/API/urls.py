from django.urls import path
from .views import CounselorAllPatient
urlpatterns=[
    path('counselorallpatient',CounselorAllPatient.as_view()),
    # path('SetAppointment',SetAppointment.as_view())
]