from django.urls import path
from .views import RegisterApi
urlpatterns=[
    path('Register',RegisterApi.as_view())
]