from datetime import datetime,timedelta

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.serializers import Serializer,EmailField,CharField,BooleanField,DateTimeField
from Counselor.models import CounselorAppointment
from Account.models import CustomUser
from Questions.models import SelfAssessment
from ..models import DoctorAppointment

class DoctorPatientSerializer(Serializer):
    id=CharField(required=True)
    Doctor=EmailField(read_only=True)
    Patient=EmailField(required=True)
    Firstname=CharField(read_only=True)
    Lastname=CharField(read_only=True)
    Accept=BooleanField(required=True)
    Appointment=DateTimeField(allow_null=True,required=True)
    Description=CharField(allow_null=True,allow_blank=True,required=True)
    def to_representation(self, instance):
        data=super().to_representation(instance)
        data['Firstname']=instance.Firstname
        data['Lastname']=instance.Lastname
        return data
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.error=False
    def validate(self, data):
        accept = data.get('Accept')
        appointment = data.get('Appointment')
        patient = data.get('Patient')
        selected_patient = DoctorAppointment.objects.filter(Patient__email=patient)
        id = data.get('id')
        selected_appointment = DoctorAppointment.objects.filter(id=id)
        if selected_appointment.first() is None:
            self.error = True
            raise ValidationError({"Error": "check the id that you are sending, it was wrong"})
        if not selected_patient.first():
            raise ValidationError({"Error": "this patient is not assigned to any doctor by counselor yet"})
        if accept == False:
            if appointment is not None:
                self.error = True
                raise ValidationError({"Error": "you are setting Accept as False and assigning an Appointment,Wrong "})
        if accept == True:
            if appointment is None:
                self.error=True
                raise ValidationError(
                    {"Error": f"You are accepting{patient} so you have to set an appointment with him "})
        if appointment is None:
            if accept == True:
                self.error = True
                raise ValidationError({"Error": "you are setting Accept as True and  the Appointment as Null,Wrong "})
        if appointment:
            if accept == False:
                self.error=True
                raise ValidationError(
                    {"Error": f"You are accepting{patient} so you have to set accept as True "})

        return True
    def validate_id(self,value):

        if value is None:
            raise ValidationError({"Error":"this field is required"})
        return value
    def update(self,validated_data,doctor):
        id=validated_data.get('id')
        patient=validated_data.get('Patient')
        Accept=validated_data.get('Accept')
        appointment=validated_data.get('Appointment')
        description=validated_data.get('Description')
        authuser=self.context['authuser']
        selected_doctor_patient=DoctorAppointment.objects.filter(id=id)
        if selected_doctor_patient.first().Accept==False:
            return Response({"Error":f"the patient {patient} was already rejected by {selected_doctor_patient.first().Doctor.email}"},status=status.HTTP_400_BAD_REQUEST)
        if selected_doctor_patient.first().Doctor.email!=authuser.email:
            return Response({"Error":f"this patient {patient} was assigned to {selected_doctor_patient.first().Doctor},you dont have permission  "},status=status.HTTP_400_BAD_REQUEST)
        if Accept==False:
            if description is not None:
                CustomUser.objects.filter(email__exact=patient).update(assessment=False)

                DoctorAppointment.objects.filter(id=id).update(
                    Accept=Accept,Description=description,Appointment=None
                )
                return Response({"detail":f"patient is rejected by {authuser.email}"},status=status.HTTP_200_OK)
            else:

                return Response({"Error":f"Doctor {authuser.email} is rejecting patient {patient} ,please provide a description for it"},status=status.HTTP_400_BAD_REQUEST)

        if selected_doctor_patient.first().Appointment is None:
            has_appointment = self.check_appointment(appointment=appointment, doctor=doctor)
            if has_appointment==True:
                return Response({"Error":f"have another appointment in {self.selected_next_appointmet.time()} on {self.selected_next_appointmet.day}th"},status=status.HTTP_400_BAD_REQUEST)
            else:
                updated_appointment=DoctorAppointment.objects.filter(
                    id=id

                ).update(Appointment=appointment,Accept=Accept,Description=description)
                selected_appointment=DoctorAppointment.objects.filter(id=id).first()
                return Response({"id":selected_appointment.id,
                                 "Doctor":selected_appointment.Doctor.email,
                                 "Patient":selected_appointment.Patient.email,
                                 "Firstname":selected_appointment.Patient.first_name,
                                 "Lastname":selected_appointment.Patient.last_name,
                                 "Status":selected_appointment.Accept,
                                 "Appointment":selected_appointment.Appointment,
                                 "Description":selected_appointment.Description},status=status.HTTP_201_CREATED)
        else:
            selected_doctor=selected_doctor_patient.first().Doctor.email
            has_appointment = self.check_appointment(appointment=appointment, doctor=doctor)
            if selected_doctor==authuser.email:

                if has_appointment == True:
                    return Response({
                                        "Error": f"have another appointment in {self.selected_next_appointmet.time()} on {self.selected_next_appointmet.day}th"},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    updated_appointment = DoctorAppointment.objects.filter(
                        id=id

                    ).update(Appointment=appointment, Accept=Accept, Description=description)
                    selected_appointment = DoctorAppointment.objects.filter(id=id).first()
                    return Response({"id": selected_appointment.id,
                                     "Doctor": selected_appointment.Doctor.email,
                                     "Patient": selected_appointment.Patient.email,
                                     "Firstname": selected_appointment.Patient.first_name,
                                     "Lastname": selected_appointment.Patient.last_name,
                                     "Status": selected_appointment.Accept,
                                     "Appointment": selected_appointment.Appointment,
                                     "Description": selected_appointment.Description}, status=status.HTTP_201_CREATED)
            else:
                return Response({"Error":f"Patient {patient} has another meeting on {selected_doctor_patient.first().Appointment.day}th at {selected_doctor_patient.first().Appointment.time()}"},status=status.HTTP_400_BAD_REQUEST)

    def check_appointment(self, appointment, doctor):
        selected_time = appointment.split('T')
        time_obj = datetime.strptime(selected_time[1], '%H:%M:%S')
        next_obj_time = time_obj + timedelta(hours=1)
        pre_obj_time = time_obj - timedelta(hours=1)
        next_time_str = next_obj_time.strftime("%H:%M:%S")
        pre_obj_str = pre_obj_time.strftime("%H:%M:%S")
        next_appointment = selected_time[0] + "T" + next_time_str
        pre_appointment = selected_time[0] + "T" + pre_obj_str
        selected_appointment = DoctorAppointment.objects.filter(Doctor_id=doctor.id,
                                                                   Appointment__lte=next_appointment,
                                                                   Appointment__gte=pre_appointment)
        if selected_appointment.first() is None:
            return False
        else:
            self.selected_next_appointmet = selected_appointment.first().Appointment
            return True


class DoctorCreateNewAppointment(Serializer):
    Patient = EmailField(required=True)
    Appointment = DateTimeField(allow_null=False, required=True)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.error=False
    def validate(self, data):
        appointment=data.get('Appointmen')
        authuser=self.context['authuser']
        patient=data.get('Patient')
        selected_appointment=DoctorAppointment.objects.filter(Doctor_id=authuser.id,Appointment=appointment)
        selected_patient_from_table=DoctorAppointment.objects.filter(Patient__email=patient)
        if selected_patient_from_table.first() is None:
            self.error=True
            raise ValidationError({"Error":f"you cant create a meeting with this patient {patient} because this patient is not assigned to any doctor yet"})
        if selected_appointment.first():
            self.error=True
            raise ValidationError({"Error":f"You have another meeting in this time with {selected_appointment.first().Patient.email}"})
        return True
    def create(self, validated_data):
        doctor=self.context['authuser']
        appointment=validated_data.get('Appointment')
        pateint=validated_data.get('Patient')
        has_appointment=self.check_appointment(appointment=appointment,doctor=doctor)
        if has_appointment==True:
            return Response({"Error": f"have another appointment in {self.selected_next_appointmet.time()} on {self.selected_next_appointmet.day}th"},
                            status=status.HTTP_400_BAD_REQUEST)
        else:

            created_app=DoctorAppointment.objects.create(
                Appointment=appointment,
                Doctor_id=doctor.id,
                Patient_id=CustomUser.objects.filter(email__exact=pateint).first().id
            )
            selected_appointment=DoctorAppointment.objects.filter(id=created_app.id).first()
            return Response({"Patient":selected_appointment.Patient.email,
                             "Doctor":selected_appointment.Doctor.email,
                             "Appointment":selected_appointment.Appointment,
                             "Accept":selected_appointment.Accept,
                             "Description":selected_appointment.Description},status=status.HTTP_201_CREATED)

    def check_appointment(self, appointment, doctor):
        selected_time = appointment.split('T')
        time_obj = datetime.strptime(selected_time[1], '%H:%M:%S')
        next_obj_time = time_obj + timedelta(hours=1)
        pre_obj_time = time_obj - timedelta(hours=1)
        next_time_str = next_obj_time.strftime("%H:%M:%S")
        pre_obj_str = pre_obj_time.strftime("%H:%M:%S")
        next_appointment = selected_time[0] + "T" + next_time_str
        pre_appointment = selected_time[0] + "T" + pre_obj_str
        selected_appointment = DoctorAppointment.objects.filter(Doctor_id=doctor.id,
                                                                Appointment__lte=next_appointment,
                                                                Appointment__gte=pre_appointment)
        if selected_appointment.first() is None:
            return False
        else:
            self.selected_next_appointmet = selected_appointment.first().Appointment
            return True