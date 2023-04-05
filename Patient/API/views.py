import json

from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from Counselor.models import CounselorAppointment
from Doctors.models import DoctorAppointment
from Account.models import CustomUser
from Questions.models import SelfAssessment
from .Serializer import PatientwithDoctorSerializer, Patien_witht_CounselorAppointmentSerialzier, \
    AppointmentRejectionDoctorSerializer, AppointmentRejectionCounselorSerializer
from .Permissions import PatientBasePermission
class ParentPatientApi(ListAPIView):
    permission_classes = [PatientBasePermission]

    authuser=None
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        token = self.request.headers['Authorization'].split(' ')[1]
        if (token):
            selected_token = Token.objects.filter(key__exact=token).first()
            selected_user = CustomUser.objects.filter(id=selected_token.user.id).first()
            self.authuser = selected_user
            self.request.user = self.authuser
        self.check_permissions(self.request)
class GetPatientAppointmentwithCounselorApi(ParentPatientApi):
    serializer_class =Patien_witht_CounselorAppointmentSerialzier
    def get_queryset(self):
        queryset=CounselorAppointment.objects.filter(Patient_id=self.authuser.id).all()
        return queryset
class GetPateintAppointmentwithDoctor(ParentPatientApi):
    serializer_class = PatientwithDoctorSerializer
    def get_queryset(self):
        queryset=DoctorAppointment.objects.filter(Patient_id=self.authuser.id).all()
        return queryset

class RejectAppointmentwithDocotrApi(ListAPIView):
    serializer_class = AppointmentRejectionDoctorSerializer
    permission_classes = [PatientBasePermission]
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
    def get(self, request, *args, **kwargs):
        raise MethodNotAllowed(self.request)
    def post(self,request,*args,**kwargs):
        raise MethodNotAllowed(self.request)
    def delete(self,request,*args,**kwargs):
        raise MethodNotAllowed(self.request)
    def put(self,request,*args,**kwargs):
        serializer=AppointmentRejectionDoctorSerializer(data=self.request.data)
        serializer.context['authuser']=self.authuser
        if(serializer.is_valid()):
            id=self.request.data.get('id')
            accept=self.request.data.get('Accept')
            desc=self.request.data.get('Description')
            rejected = False
            assessment = True
            if (accept == True):
                rejected = False
                assessment = True
            else:
                assessment = False
                rejected = True
            update_selected_appointment=DoctorAppointment.objects.filter(id=id).update(
                Accept=accept,
                Description=desc,RejectedByPatient=rejected
            )
            selected_selfassessment=CustomUser.objects.filter(email__exact=self.authuser.email).update(
                assessment=assessment
            )
            selected_appointment=DoctorAppointment.objects.filter(id=id)
            serializer_data=AppointmentRejectionDoctorSerializer(selected_appointment,many=True)
            return Response(serializer_data.data,status=status.HTTP_200_OK)
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



class RejectAppointmentwithCounselorApi(ListAPIView):
    serializer_class = AppointmentRejectionCounselorSerializer
    permission_classes = [PatientBasePermission]
    authuser = None

    def get(self, request, *args, **kwargs):
        raise MethodNotAllowed(self.request)

    def post(self, request, *args, **kwargs):
        raise MethodNotAllowed(self.request)

    def delete(self, request, *args, **kwargs):
        raise MethodNotAllowed(self.request)
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        token = self.request.headers['Authorization'].split(' ')[1]
        if (token):
            selected_token = Token.objects.filter(key__exact=token).first()
            selected_user = CustomUser.objects.filter(id=selected_token.user.id).first()
            self.authuser = selected_user
            self.request.user = self.authuser
        self.check_permissions(self.request)
    def put(self,request,*args,**kwargs):
        serializer=AppointmentRejectionCounselorSerializer(data=self.request.data)
        serializer.context['authuser']=self.authuser
        if(serializer.is_valid()):
            id=self.request.data.get('id')
            accept=self.request.data.get('Accept')
            desc=self.request.data.get('Description')
            rejected=False
            assessment=True
            if(accept==True):
                rejected=False
                assessment=True
            else:
                assessment=False
                rejected=True
            update_selected_appointment=CounselorAppointment.objects.filter(id=id).update(
                Accept=accept,
                Description=desc,RejectedByPatient=rejected
            )
            selected_assessment=CustomUser.objects.filter(email__exact=self.authuser.email).update(
                assessment=assessment
            )
            selected_appointment=CounselorAppointment.objects.filter(id=id)
            serializer_data=AppointmentRejectionCounselorSerializer(selected_appointment,many=True)
            return Response(serializer_data.data,status=status.HTTP_200_OK)
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
# Create your views here.
