import json

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from Doctors.models import DoctorAppointment
from .serializer import PatientCounselorAppointmentSerialzier, CounselorMangeDoctors, ListofDoctorsSerializer
from .permission import CounselorPermission
from Account.models import CustomUser
from Counselor.models import CounselorAppointment
class ParentSerializer(ListAPIView):
    permission_classes = [CounselorPermission]
    authuser=None
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        token = self.request.headers['Authorization'].split(' ')[1]
        selected_token = Token.objects.filter(key__exact=token).first()
        if selected_token:
            self.authuser = CustomUser.objects.filter(id=selected_token.user.id)
            self.request.user = self.authuser.first()
        self.check_permissions(self.request)
class CounselorAllPatient(ListAPIView):
    serializer_class = PatientCounselorAppointmentSerialzier
    authuser=None
    permission_classes = [CounselorPermission]
    def get_serializer_context(self):
        context=super().get_serializer_context()
        allpatients=CounselorAppointment.objects.all()
        context['allpatients']=allpatients
        return context
    def initial(self, request, *args, **kwargs):
        super().initial(request,*args,**kwargs)
        token=self.request.headers['Authorization'].split(' ')[1]
        selected_token=Token.objects.filter(key__exact=token).first()
        if selected_token:
            self.authuser=CustomUser.objects.filter(id=selected_token.user.id)
            self.request.user=self.authuser.first()
        self.check_permissions(self.request)

    def get_queryset(self):
        queryset=CounselorAppointment.objects.all()
        for obj in queryset:
            obj.Firstname=CustomUser.objects.filter(email__exact=obj.Patient.email).first()
            obj.Lastname = CustomUser.objects.filter(email__exact=obj.Patient.email).first()
        return queryset
    def put(self,request,*args,**kwargs):
        data=self.request.data
        serializer=PatientCounselorAppointmentSerialzier(data=data)
        if serializer.is_valid():
            return serializer.update(counselor=self.authuser.first(),validated_data=data)
        else:
                error = json.dumps(serializer.errors)
                err = json.loads(error)
                send_error = None
                if getattr(serializer, 'error'):
                    json_error = err["Error"][0]
                    send_error = {"Error": json_error}
                else:
                    send_error = serializer.errors
                return Response(send_error,status=status.HTTP_400_BAD_REQUEST)

class CounselorMangeDoctorApi(ListAPIView):
    serializer_class = CounselorMangeDoctors
    permission_classes = [CounselorPermission]
    authuser=None
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        token = self.request.headers['Authorization'].split(' ')[1]
        selected_token = Token.objects.filter(key__exact=token).first()
        if selected_token:
            self.authuser = CustomUser.objects.filter(id=selected_token.user.id)
            self.request.user = self.authuser.first()
        self.check_permissions(self.request)
    def put(self,request,*args,**kwargs):
        data=self.request.data
        serializer=CounselorMangeDoctors(data=data)
        serializer.context["authuser"] = self.authuser
        if serializer.is_valid():
            return serializer.create(validated_data=data)
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

class ListofDoctorsAi(ListAPIView):
    serializer_class = ListofDoctorsSerializer
    permission_classes = [CounselorPermission]
    def initial(self, request, *args, **kwargs):
        super().initial(request,*args,**kwargs)
        token=self.request.headers['Authorization'].split(' ')[1]
        selected_token=Token.objects.filter(key__exact=token).first()
        if selected_token:
            self.authuser=CustomUser.objects.filter(id=selected_token.user.id)
            self.request.user=self.authuser.first()
        self.check_permissions(self.request)

    def get_queryset(self):
        queryset=CustomUser.objects.filter(role__exact='doctor').all()
        return queryset


class CounselorPatientAppointmentApi(ParentSerializer):
    serializer_class = PatientCounselorAppointmentSerialzier
    permission_classes = [CounselorPermission]
    def initial(self, request, *args, **kwargs):

        super().initial(request, *args, **kwargs)
        token = self.request.headers['Authorization'].split(' ')[1]
        selected_token = Token.objects.filter(key__exact=token).first()
        if selected_token:
            self.authuser = CustomUser.objects.filter(id=selected_token.user.id)
            self.request.user = self.authuser.first()
        self.check_permissions(self.request)
    def get_queryset(self):
        data=self.request.GET
        if (data.get('appointment')) is None:
            raise ValidationError({"Error": "You need to set a data in request params"})

        appointment=data.get('appointment')
        self.query=CounselorAppointment.objects.filter(
            Counselor_id=self.authuser.first().id,Appointment__date=appointment
        ).all()
        for obj in self.query:
            obj.Firstname=self.query.filter(id=obj.id).first().Patient
            obj.Lastname=self.query.filter(id=obj.id).first().Patient
        return self.query





