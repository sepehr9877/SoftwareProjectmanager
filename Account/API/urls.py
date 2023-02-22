from django.urls import path
from .views import RegisterApi,UpdateUserApi,CounselorPatientsApi
urlpatterns=[
    path('Register',RegisterApi.as_view()),
    path('UpdateUserApi/<int:id>',UpdateUserApi.as_view()),
    path('getAllPatients',CounselorPatientsApi.as_view())
]