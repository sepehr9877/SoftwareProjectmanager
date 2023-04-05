from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer, CharField, EmailField, BooleanField, DateTimeField, ModelSerializer

from Counselor.models import CounselorAppointment
from Doctors.models import DoctorAppointment


class PatientwithDoctorSerializer(Serializer):
    id=CharField(read_only=True)
    Doctor=EmailField(read_only=True)
    Patient=EmailField(read_only=True)
    Firstname=CharField(read_only=True)
    Lastname=CharField(read_only=True)
    Accept=BooleanField(required=True)
    Appointment=DateTimeField(allow_null=True,required=True)
    Description=CharField(allow_null=True,allow_blank=True,required=True)

class Patien_witht_CounselorAppointmentSerialzier(Serializer):
    id=CharField(required=True)
    Patient = EmailField(required=True)
    Firstname=CharField(read_only=True)
    Lastname=CharField(read_only=True)
    Appointment = DateTimeField(allow_null=True,required=True)
    Accept = BooleanField(allow_null=False,required=True)
    Description =CharField(max_length=100,allow_null=True,allow_blank=True,required=True)
    Doctor=EmailField(read_only=True)
    AssigntoDoctor=BooleanField(read_only=True)
    Counselor=EmailField(read_only=True,allow_null=True)
    Doctor=EmailField(read_only=True,allow_null=True)


class AppointmentRejectionDoctorSerializer(Serializer):
    id = CharField(required=True)
    Doctor=EmailField(read_only=True)
    Patient=EmailField(read_only=True)
    Accept =BooleanField(required=True)
    Appointment=DateTimeField(read_only=True)
    Description=CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error = False
    def validate(self, data):
        id=data.get('id')
        selected_patient=DoctorAppointment.objects.filter(id=id)
        if(selected_patient.first() is None):
            self.error=True
            raise ValidationError({"Error":"You are sending a wrong id"})
        if (selected_patient.first().Accept == False):
            self.error = True
            raise ValidationError({"Error": "This Appointment was already rejected and you cant modify it"})
        authuser=self.context['authuser']
        if(selected_patient.first().Patient.email==authuser.email):
            return True
        else:
            self.error=True
            raise ValidationError({"Error":"This Appointment is for another patient"})



class AppointmentRejectionCounselorSerializer(Serializer):
    id = CharField(required=True)
    Doctor=EmailField(read_only=True)
    Patient=EmailField(read_only=True)
    Accept =BooleanField(required=True)
    Appointment=DateTimeField(read_only=True)
    Description=CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error = False
    def validate(self, data):
        id=data.get('id')
        selected_patient=CounselorAppointment.objects.filter(id=id)

        if(selected_patient.first() is None):
            self.error=True
            raise ValidationError({"Error":"You are sending a wrong id"})
        if(selected_patient.first().Accept==False):
            self.error=True
            raise ValidationError({"Error":"This Appointment was already rejected and you cant modify it"})
        authuser=self.context['authuser']
        if(selected_patient.first().Patient.email==authuser.email):
            return True
        else:
            self.error=True
            raise ValidationError({"Error":"This Appointment is for another patient"})