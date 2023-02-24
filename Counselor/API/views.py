from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .serializer import CounselorPatientAppointmentSerializer
from .permission import CounselorPermission
from Account.models import CustomUser
from Counselor.models import CounselorAppointment
class CounselorPatientApi(ListAPIView):
    serializer_class = CounselorPatientAppointmentSerializer
    permission_classes =(CounselorPermission,)
    authuser=None
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        token_authorization=self.request.headers['Authorization'].split(' ')[1]
        selected_token=Token.objects.filter(key__exact=token_authorization).first()
        if selected_token:
            selected_user=CustomUser.objects.filter(id=selected_token.user.id)
            if selected_user:
                self.request.user=selected_user.first()
                self.authuser=selected_user
        self.check_permissions(self.request)
    def get_queryset(self):
        email=self.request.data.get('email')
        selected_patient=None
        if email:
            selected_patient=CounselorAppointment.objects.filter(Patients__email=email,Counselor__email=self.authuser.first().email)
        else:
            selected_patient=CounselorAppointment.objects.all()
        return selected_patient
    def post(self,request,*args,**kwargs):
        data=self.request.data
        seralizer=CounselorPatientAppointmentSerializer(data=data)
        if seralizer.is_valid():
            created_patient=seralizer.create(validated_data=self.request.data)
            if created_patient:
                return Response({
                    "AppointmentID":created_patient.first().id,
                    "Patients":created_patient.first().Patients.email,
                    "Counselor":created_patient.first().Counselor.email,
                    "Appointment":created_patient.first().Appointment},status=status.HTTP_201_CREATED)
            else:
                return Response({"Patients":"Assign to Doctor"},status=status.HTTP_200_OK)
        else:
            return Response({"Error":seralizer.errors},status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
