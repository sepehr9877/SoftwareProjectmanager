from django.contrib.auth import authenticate, login
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,UpdateModelMixin,DestroyModelMixin,RetrieveModelMixin
from rest_framework.response import Response

from Account.models import CustomUser
from .serializer import  RegistrationSeralizer
class RegisterApi(ListAPIView):
    serializer_class = RegistrationSeralizer
    def get_queryset(self):None
    def post(self,request,*args,**kwargs):
        data=self.request.data
        serializer=RegistrationSeralizer(data=data)
        if serializer.is_valid():
            email,password=serializer.create(validated_data=data)
            auth=authenticate(self.request,email=email,password=password)
            login(request=self.request,user=auth)
            return Response({"Success":"User Register"},status=status.HTTP_200_OK)
        else:
            return Response({"Error": serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Create your views here.
