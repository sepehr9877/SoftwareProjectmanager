import calendar
import json

from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import MethodNotAllowed, ValidationError
from rest_framework.response import Response

from Account.models import CustomUser
from Counselor.models import CounselorAppointment
from Doctors.models import DoctorAppointment
from Questions.models import SelfAssessment
from .permissions import ManagerPermission
from rest_framework.generics import ListAPIView
from .Serializers import AcceptRejectDoctorSerializer, AcceptRejectCounselorSerializer, \
    ManagerDateDocotorPatientSerializer, AcceptRejectPatientSerializer, MangerBussinessInfo


class AcceptRejectParentApi(ListAPIView):
    authuser=None
    def initial(self, request, *args, **kwargs):

        super().initial(request, *args, **kwargs)
        token = self.request.headers['Authorization'].split(' ')[1]

        selected_token = Token.objects.filter(key__exact=token).first()
        if selected_token:
            self.authuser = CustomUser.objects.filter(id=selected_token.user.id)
            self.request.user = self.authuser.first()
        self.check_permissions(self.request)
    def get_queryset(self):
        raise MethodNotAllowed(self.request.method)




class AcceptRejectDoctorApi(AcceptRejectParentApi):
    serializer_class = AcceptRejectDoctorSerializer
    permission_classes = [ManagerPermission]
    def get_queryset(self):
        query=CustomUser.objects.filter(role__exact='doctor').all()
        return query
    def put(self, request, *args, **kwargs):
        data=self.request.data
        serializer=AcceptRejectDoctorSerializer(data=data)
        if serializer.is_valid():
            return serializer.update(manager=self.authuser,validated_data=data)
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

class AcceptRejectCounselorApi(AcceptRejectParentApi):
    serializer_class = AcceptRejectCounselorSerializer
    permission_classes = [ManagerPermission]
    def get_queryset(self):
        query=CustomUser.objects.filter(role__exact='counselor').all()
        return query
    def put(self, request, *args, **kwargs):
        data=self.request.data
        serializer=AcceptRejectCounselorSerializer(data=data)
        if serializer.is_valid():
            return serializer.update(manager=self.authuser,validated_data=data)
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
class ManagerGetPatientOfDoctorByDate(AcceptRejectParentApi):
    serializer_class = ManagerDateDocotorPatientSerializer
    def get_queryset(self):
        exact=str(self.request.GET.get('exactdate'))
        week = int(self.request.GET.get('week'))
        year = int(self.request.GET.get("year"))
        month = int(self.request.GET.get('month'))
        if(week>5 or week<1):
            raise ValidationError({"Error":"Week should be between 1 and 5"})
        if (month==0and week==0 and year==0 and exact=="0"):
            raise ValidationError({"Error":"all fields are Zero"})
        if(exact!="0" and(month!=0 or week!=0 or year!=0)):
            raise ValidationError({"Error":"Check your fields you either can get patients by exact date or by month of year or by week of the month in some year"})
        if((month!=0 or week!=0) and year==0):
            raise  ValidationError({"Error":"you have to mention the specific year to get patient in the specific  week or month"})
        if((week!=0 )and (month==0 or year==0)):
            raise ValidationError({"Error":"you need to set year and month to get patients in a specific weeko"})
        patient=None
        if exact!="0":
            patient=DoctorAppointment.objects.filter(Appointment__date=exact)

        else:

            appointmentlte = str(year)+"-"+str(month)
            appointmentgte = str(year)+"-"+str(month)
            if week !=0:
                let_day=(week-1)*7+1
                if(week==5):
                    gte_day=calendar.monthrange(year,month)[1]
                else:
                    gte_day = (week) * 7
                appointmentlte=appointmentlte+"-"+str(let_day)
                appointmentgte=appointmentgte+"-"+str(gte_day)
                patient = DoctorAppointment.objects.filter(Appointment__date__gte=appointmentlte,
                                                           Appointment__date__lte=appointmentgte).all()
            if week==0:
                if month!=0:
                    patient = DoctorAppointment.objects.filter(Appointment__month=month,Appointment__year=year).all()


        return patient







class ManagerGetPatientofCounselorByDate(AcceptRejectParentApi):
    serializer_class = ManagerDateDocotorPatientSerializer
    def get_queryset(self):
        exact=str(self.request.GET.get('exactdate'))
        week = int(self.request.GET.get('week'))
        year = int(self.request.GET.get("year"))
        month = int(self.request.GET.get('month'))
        if(week>5 or week<0):
            raise ValidationError({"Error":"Week should be between 1 and 5"})
        if (month==0and week==0 and year==0 and exact=="0"):
            raise ValidationError({"Error":"all fields are Zero"})
        if(exact!="0" and(month!=0 or week!=0 or year!=0)):
            raise ValidationError({"Error":"Check your fields you either can get patients by exact date or by month of year or by week of the month in some year"})
        if((month!=0 or week!=0) and year==0):
            raise  ValidationError({"Error":"you have to mention the specific year to get patient in the specific  week or month"})
        if((week!=0 )and (month==0 or year==0)):
            raise ValidationError({"Error":"you need to set year and month to get patients in a specific weeko"})
        patient=None
        if exact!="0":
            patient=CounselorAppointment.objects.filter(Appointment__date=exact)

        else:

            appointmentlte = str(year)+"-"+str(month)
            appointmentgte = str(year)+"-"+str(month)
            if week !=0:
                let_day=(week-1)*7+1
                if(week==5):
                    gte_day=calendar.monthrange(year,month)[1]
                else:
                    gte_day = (week) * 7
                appointmentlte=appointmentlte+"-"+str(let_day)
                appointmentgte=appointmentgte+"-"+str(gte_day)
                patient = CounselorAppointment.objects.filter(Appointment__date__gte=appointmentlte,
                                                           Appointment__date__lte=appointmentgte).all()
            if week==0:
                if month!=0:
                    patient = CounselorAppointment.objects.filter(Appointment__month=month,Appointment__year=year).all()


        return patient


class MangerAcceptRejectPatients(AcceptRejectParentApi):
    serializer_class = AcceptRejectDoctorSerializer
    permission_classes = [ManagerPermission]

    def get_queryset(self):
        query = CustomUser.objects.filter(role__exact='patient').all()
        return query

    def put(self, request, *args, **kwargs):
        data = self.request.data
        serializer = AcceptRejectPatientSerializer(data=data)
        if serializer.is_valid():
            return serializer.update(manager=self.authuser, validated_data=data)
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

class ManagerGetInfoAPi(ListAPIView):
    serializer_class = MangerBussinessInfo
    permission_classes = [ManagerPermission]
    def initial(self, request, *args, **kwargs):
        token = self.request.headers['Authorization'].split(' ')[1]

        selected_token = Token.objects.filter(key__exact=token).first()
        if selected_token:
            self.authuser = CustomUser.objects.filter(id=selected_token.user.id)
            self.request.user = self.authuser.first()
        self.check_permissions(self.request)
    def get(self, request, *args, **kwargs):
        all_users=CustomUser.objects.all()
        all_patients=all_users.filter(role__exact='patient')
        number_of_acceptedpatients=all_users.filter(role__exact='patient',accept=True).count()
        number_of_acceptedcounselors=all_users.filter(role__exact='counselor',accept=True).count()
        number_of_rejectedpatients=all_users.filter(role__exact='patient',accept=True).count()
        number_of_rejectedcounselors=all_users.filter(role__exact='counselor',accept=False).count()
        all_doctors=CustomUser.objects.filter(role__exact='doctor').all()
        all_counselors=CustomUser.objects.filter(role__exact='counselor').all()
        number_of_active_doctors=DoctorAppointment.objects.filter(Doctor__in=all_doctors).values_list('Doctor__email',flat=True).distinct()
        number_of_inactive_doctors=all_doctors.exclude(email__in=number_of_active_doctors).values_list('email',flat=True).distinct()
        number_of_active_doctors=number_of_active_doctors.count()
        number_of_inactive_doctors=number_of_inactive_doctors.count()
        number_of_active_counselors=CounselorAppointment.objects.filter(Counselor__in=all_counselors).values_list('Counselor__email',flat=True).distinct()
        number_of_inactive_counselors=all_counselors.exclude(email__in=number_of_active_counselors).values_list('email',flat=True).distinct()
        number_of_active_counselors=number_of_active_counselors.count()
        numbers_of_selfassessments=SelfAssessment.objects.filter().values_list('Patient__email',flat=True)
        number_of_patients_withot_selfasssessment=all_patients.exclude(email__in=numbers_of_selfassessments).count()
        number_of_inactive_counselors=number_of_inactive_counselors.count()
        numbers_of_patients_appointment_counselors=CounselorAppointment.objects.filter(Patient__in=all_patients,Appointment__isnull=False).count()

        return Response({"number_of_acceptedpatients":number_of_acceptedpatients,
                         "number_of_acceptedcounselors":number_of_acceptedcounselors,
                         "number_of_rejectedpatients":number_of_rejectedpatients,
                         "number_of_rejectedcounselors":number_of_rejectedcounselors,
                         "number_of_patients_without_selfasssessment":number_of_patients_withot_selfasssessment,
                         "numbers_of_patients_appointment_counselors":numbers_of_patients_appointment_counselors,
                         "all_doctors":all_doctors.count(),
                         "all_counselors":all_counselors.count(),
                         "number_of_active_doctors":number_of_active_doctors,
                         "number_of_inactive_doctors":number_of_inactive_doctors,
                         "number_of_inactive_counselors":number_of_inactive_counselors,
                         "number_of_active_counselors":number_of_active_counselors})
