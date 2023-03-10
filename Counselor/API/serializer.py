from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer,EmailField,DateTimeField,BooleanField,CharField
from Account.models import CustomUser
from Counselor.models import CounselorAppointment
from Doctors.models import DoctorAppointment
from Questions.models import SelfAssessment

class PatientCounselorAppointmentSerialzier(Serializer):
    Patient = EmailField(required=True)
    Firstname=CharField(read_only=True)
    Lastname=CharField(read_only=True)
    Appointment = DateTimeField(allow_null=True,required=True)
    Accept = BooleanField(allow_null=False,required=True)
    Description =CharField(max_length=100,allow_null=True,allow_blank=True,required=True)
    Doctor=EmailField(read_only=True)
    AssigntoDoctor=BooleanField(read_only=True)
    Counselor=EmailField(read_only=True,allow_null=True)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.error = False
    def validate(self, data):
        accept=data.get('Accept')
        appointment=data.get('Appointment')
        patient=data.get('Patient')
        selected_patient=CounselorAppointment.objects.filter(Patient__email=patient)
        if not selected_patient.first():
            raise  ValidationError({"Error":"this patient has not completed the self assessment yet"})
        if accept==False:
            if appointment is not None:
                self.error = True
                raise ValidationError({"Error":"you are setting Accept as False and assigning an Appointment,Wrong "})
        if accept==True:
            if appointment is None:
                raise ValidationError({"Error":f"You are accepting{patient} so you have to set an appointment with him "})
        if appointment is None:
            if accept==True:
                self.error = True
                raise ValidationError({"Error": "you are setting Accept as True and  the Appointment as Null,Wrong "})
        if appointment:
            if accept==False:
                raise ValidationError(
                    {"Error": f"You are accepting{patient} so you have to set accept as True "})
        return data

    def to_representation(self, instance):
        data=super().to_representation(instance)
        data['Doctor']=instance.Doctor.Doctor.email if instance.Doctor else None
        data['Firstname']=instance.Firstname.first_name
        data['Lastname']=instance.Lastname.last_name
        return data
    def update(self, counselor, validated_data):
        appointment=validated_data.get('Appointment')
        Accept=validated_data.get('Accept')
        PatientEmail=validated_data.get('Patient')
        Description=validated_data.get('Description')
        selected_appointment=CounselorAppointment.objects.filter(
            Counselor_id=counselor.id,
            Patient__email=PatientEmail
        )
        if selected_appointment.first():
            return Response({"Error":f"the pateint {PatientEmail} and"
                              f" the counselor {selected_appointment.first().Counselor.email} "
                              f"have meeting together"},status=status.HTTP_400_BAD_REQUEST)
        else:
            has_appointment=self.check_appointment(counselor=counselor,appointment=appointment)
            if has_appointment==True:
                return Response({
                                    "Error": f"have another appointment at {self.selected_next_appointmet.time()} on {self.selected_next_appointmet.day}th"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:

                CounselorAppointment.objects.filter(

                    Patient__email=PatientEmail
                ).update(
                    Counselor_id=counselor.id,
                    Appointment=appointment,Accept=Accept,Description=Description
                )
                selected_counselor_appointment=CounselorAppointment.objects.filter(
                    Patient__email=PatientEmail,Counselor_id=counselor.id,Appointment=appointment
                ).first()
                return Response({"Patient":selected_counselor_appointment.Patient.email,
                                 "Counselor":selected_counselor_appointment.Counselor.email,
                                 "Appointment":selected_counselor_appointment.Appointment,
                                 "Accept":selected_counselor_appointment.Accept,
                                 "AssigntoDoctor":selected_counselor_appointment.AssigntoDoctor},status=status.HTTP_200_OK)
    def check_appointment(self,appointment,counselor):
        selected_time = appointment.split('T')
        time_obj = datetime.strptime(selected_time[1], '%H:%M:%S')
        next_obj_time = time_obj + timedelta(hours=1)
        pre_obj_time=time_obj - timedelta(hours=1)
        next_time_str = next_obj_time.strftime("%H:%M:%S")
        pre_obj_str = pre_obj_time.strftime("%H:%M:%S")
        next_appointment = selected_time[0] + "T" + next_time_str
        pre_appointment=selected_time[0] + "T" + pre_obj_str
        selected_appointment=CounselorAppointment.objects.filter(Counselor_id=counselor.id,Appointment__lte=next_appointment,Appointment__gte=pre_appointment)
        if selected_appointment.first() is None:
            return False
        else:
            self.selected_next_appointmet=selected_appointment.first().Appointment
            return True



class CounselorMangeDoctors(Serializer):
    Doctor=EmailField(required=True)
    Patient=EmailField(required=True)
    Description=CharField(required=True,allow_null=False)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.error = False
    def validate(self, data):
        doctor=data.get('Doctor')
        authuser=self.context['authuser']
        patient=data.get('Patient')
        selected_counselor_patient=CounselorAppointment.objects.filter(
            Patient__email=patient
        )
        if selected_counselor_patient.first().Counselor:
            raise ValidationError({"Error":f"{patient} has an appointment with counselor {selected_counselor_patient.first().Counselor.email}"})
        selected_patient_doctor=DoctorAppointment.objects.filter(
            Doctor__email=doctor,Patient__email=patient
        )
        if selected_patient_doctor.first():
            self.error=True
            raise ValidationError({"Error":f"{patient} was already assigned to {doctor}"})
        return True
    def create(self, validated_data):
        doctor_email=validated_data.get('Doctor')
        description=validated_data.get('Description')
        authuser=self.context['authuser']
        doctor=CustomUser.objects.filter(
            email__exact=doctor_email
        ).first()
        patient_email=validated_data.get('Patient')
        patient=CustomUser.objects.filter(
            email__exact=patient_email
        ).first()
        CounselorAppointment.objects.filter(
            Patient__email=patient_email,

        ).update(
            Counselor_id=authuser.first().id,
            Accept=True,
            AssigntoDoctor=True,
            Description=description
        )
        create_appointment_with_doctor=DoctorAppointment.objects.create(
            Doctor_id=doctor.id,Patient_id=patient.id,Accept=True
        )
        return Response({
            "Doctor":create_appointment_with_doctor.Doctor.email,
            "Patient":create_appointment_with_doctor.Patient.email,
            "Description":description,
            "Accept":create_appointment_with_doctor.Accept
        },status=status.HTTP_200_OK)

class ListofDoctorsSerializer(Serializer):
    email=EmailField(read_only=True)
    first_name=CharField(read_only=True)
    last_name=CharField(read_only=True)