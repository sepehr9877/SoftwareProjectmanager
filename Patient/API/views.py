from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from Counselor.models import CounselorAppointment
from Doctors.models import DoctorAppointment
from Account.models import CustomUser
from .Serializer import PatientwithDoctorSerializer,Patien_witht_CounselorAppointmentSerialzier
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



# Create your views here.
