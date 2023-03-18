import json

from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from Account.models import CustomUser
from ..models import DoctorAppointment
from .Serializer import DoctorPatientSerializer, DoctorCreateNewAppointment
from .permissions import DoctorPatientPermission
class DoctorParentApi(ListAPIView):
    permission_classes = [DoctorPatientPermission]
    authuser = None

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        token = self.request.headers['Authorization'].split(' ')[1]
        if (token):
            selected_token = Token.objects.filter(key__exact=token).first()
            selected_user = CustomUser.objects.filter(id=selected_token.user.id).first()
            self.authuser = selected_user
            self.request.user = self.authuser
        self.check_permissions(self.request)
class DoctorPatientApi(ListAPIView):
    serializer_class = DoctorPatientSerializer
    permission_classes = [DoctorPatientPermission]
    authuser=None
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        token=self.request.headers['Authorization'].split(' ')[1]
        if(token):
            selected_token=Token.objects.filter(key__exact=token).first()
            selected_user=CustomUser.objects.filter(id=selected_token.user.id).first()
            self.authuser=selected_user
            self.request.user=self.authuser
        self.check_permissions(self.request)

    def get_queryset(self):
        queryset=DoctorAppointment.objects.all().filter(Doctor__email=self.authuser.email)
        for obj in queryset:
            obj.Firstname=obj.Patient.first_name
            obj.Lastname=obj.Patient.last_name
        return queryset
    def put(self,request,*args,**kwargs):
        data=self.request.data
        serializer=DoctorPatientSerializer(data=data)
        serializer.context['authuser']=self.authuser
        if serializer.is_valid():
            return serializer.update(doctor=self.authuser,validated_data=data)
        else:
            error = json.dumps(serializer.errors)
            err = json.loads(error)
            send_error = None
            if getattr(serializer, 'error'):
                json_error = err["Error"][0]
                send_error = {"Error": json_error}
            else:
                send_error = serializer.errors
            return Response(send_error, status=status.HTTP_400_BAD_REQUEST)


class DoctorCreateNewAppointmentApi(ListAPIView):
    serializer_class = DoctorCreateNewAppointment
    permission_classes = [DoctorPatientPermission]
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        token = self.request.headers['Authorization'].split(' ')[1]
        if (token):
            selected_token = Token.objects.filter(key__exact=token).first()
            selected_user = CustomUser.objects.filter(id=selected_token.user.id).first()
            self.authuser = selected_user
            self.request.user = self.authuser
        self.check_permissions(self.request)

    def get_queryset(self):return None
    def post(self,request,*args,**kwargs):
        serializer=DoctorCreateNewAppointment(data=self.request.data)
        serializer.context['authuser'] = self.authuser
        if serializer.is_valid():
            return serializer.create(validated_data=self.request.data)
        else:
            error = json.dumps(serializer.errors)
            err = json.loads(error)
            send_error = None
            if getattr(serializer, 'error'):
                json_error = err["Error"][0]
                send_error = {"Error": json_error}
            else:
                send_error = serializer.errors
            return Response(send_error, status=status.HTTP_400_BAD_REQUEST)

class DoctorGetAppointmentApi(DoctorParentApi):
    serializer_class = DoctorPatientSerializer
    def get_queryset(self):
        data=self.request.data
        appointment=data.get('Appointment')
        if appointment is None:
            raise ValidationError({"Error":"set appointment in request body"})

        query=DoctorAppointment.objects.filter(Appointment__date=appointment,Doctor_id=self.authuser.id)
        for obj in query:
            obj.Firstname=query.filter(id=obj.id).first().Patient.first_name
            obj.Lastname=query.filter(id=obj.id).first().Patient.last_name
        return query

