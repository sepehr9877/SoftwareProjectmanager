import json

from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from Doctors.models import DoctorAppointment
from .serializer import PatientCounselorAppointmentSerialzier
from .permission import CounselorPermission
from Account.models import CustomUser
from Counselor.models import CounselorAppointment
# class CounselorPatientApi(ListAPIView):
#     serializer_class = CounselorPatientAppointmentSerializer
#     permission_classes =(CounselorPermission,)
#     authuser=None
#     def initial(self, request, *args, **kwargs):
#         super().initial(request, *args, **kwargs)
#         token_authorization=self.request.headers['Authorization'].split(' ')[1]
#         selected_token=Token.objects.filter(key__exact=token_authorization).first()
#         if selected_token:
#             selected_user=CustomUser.objects.filter(id=selected_token.user.id)
#             if selected_user:
#                 self.request.user=selected_user.first()
#                 self.authuser=selected_user
#         self.check_permissions(self.request)
#     def get_queryset(self):
#         self.email=self.request.data.get('email')
#         selected_patient=None
#         if self.email:
#             selected_patient=CounselorAppointment.objects.filter(Patients__email=self.email,Counselor_id=self.authuser.first().id)
#
#         else:
#             selected_patient=CounselorAppointment.objects.filter(Counselor_id=self.authuser.first().id)
#
#         return selected_patient
#
#     def delete(self,request,*args,**kwargs):
#         data=self.request.data
#         id=data.get('id')
#         Counselor_appointment=CounselorAppointment.objects.filter(id=id).first()
#         if Counselor_appointment:
#             self.check_object_permissions(self.request,obj=Counselor_appointment)
#             co=CounselorAppointment.objects.filter(id=id,Counselor_id=self.authuser.first().id).delete()
#             return Response({"success": f"the appointment with this id ={co.first().id} was deleted"},status=status.HTTP_200_OK)
#         return Response({"detail":f"there is no such an appointment with this id ={id}"},status=status.HTTP_400_BAD_REQUEST)
#
# # Create your views here.
# class SetAppointment(ListAPIView):
#     serializer_class = CounselorPatientAppointmentSerializer
#     permission_classes = (CounselorPermission,)
#     authuser=None
#     def initial(self, request, *args, **kwargs):
#         super().initial(request, *args, **kwargs)
#         token_authorization = self.request.headers['Authorization'].split(' ')[1]
#         selected_token = Token.objects.filter(key__exact=token_authorization).first()
#         if selected_token:
#             selected_user = CustomUser.objects.filter(id=selected_token.user.id)
#             if selected_user:
#                 self.request.user = selected_user.first()
#                 self.authuser = selected_user
#         self.check_permissions(self.request)
#     def get_queryset(self):
#         empty_appointment=CounselorAppointment.objects.filter(Counselor_id=None).all()
#         return empty_appointment
#     def put(self,request,*args,**kwargs):
#         data=self.request.data
#         serailizer=CounselorPatientAppointmentSerializer(data=data)
#         if serailizer.is_valid():
#             return serailizer.update(self.authuser,data)
#         else:
#             error = json.dumps(serailizer.errors)
#             err = json.loads(error)
#             send_error = None
#             if getattr(serailizer, 'error'):
#                 json_error = err["Error"][0]
#                 send_error = {"Error": json_error}
#             else:
#                 send_error = serailizer.errors
#             return Response({"detail":serailizer.errors},status=status.HTTP_400_BAD_REQUEST)


class CounselorAllPatient(ListAPIView):
    serializer_class = PatientCounselorAppointmentSerialzier
    authuser=None
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
            self.request.user=self.authuser
        self.check_permissions(self.request)

    def get_queryset(self):
        queryset=CounselorAppointment.objects.all()
        for obj in queryset:
            obj.Doctor=DoctorAppointment.objects.filter(Patient__email=obj.Patient.email).first()
            obj.Firstname=CustomUser.objects.filter(email__exact=obj.Patient.email).first()
            obj.Lastname = CustomUser.objects.filter(email__exact=obj.Patient.email).first()
        return queryset
    def put(self,request,*args,**kwargs):
        data=self.request.data
        serializer=PatientCounselorAppointmentSerialzier(data=data)
        if serializer.is_valid():
            serializer.update(counselor=self.authuser.first(),validated_data=data)
            return Response({"detail":"this appointment was update "},status=status.HTTP_200_OK)
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


