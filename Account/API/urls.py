from django.urls import path
from .views import RegisterApi,UpdateUserApi,UpdatePasswordEmailApi,LoginApi
urlpatterns=[
    path('Register',RegisterApi.as_view()),
    path('UpdateUserApi/',UpdateUserApi.as_view()),
    path('UpdatePasswordEmail',UpdatePasswordEmailApi.as_view()),
    path('login/',LoginApi.as_view())
]