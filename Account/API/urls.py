from django.urls import path
from .views import RegisterApi,UpdateUserApi
urlpatterns=[
    path('Register',RegisterApi.as_view()),
    path('UpdateUserApi/<int:id>',UpdateUserApi.as_view())
]