from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer,EmailField,DateTimeField,BooleanField,CharField
from Account.models import CustomUser
from Counselor.models import CounselorAppointment
from Questions.models import SelfAssessment
class CounselorPatientAppointmentSerializer(Serializer):
    id=CharField(read_only=True)
    Counselor=EmailField(required=False)
    Patients=EmailField(required=True)
    Appointment=DateTimeField(required=True,allow_null=True)
    AssignedToDoctor=BooleanField(read_only=True,default=False)
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error=False
    def validate(self,data):
        Patient_email=data.get('Patients')
        selected_patients=CustomUser.objects.filter(email__exact=Patient_email,role__exact="patient")
        if (selected_patients.first() is None ):
            self.error=True
            raise ValidationError({"Error":"Patient Email is Wrong "})
        return True
    def update(self, counselor, validated_data):
        Counselor_email=counselor.first().email
        Patient_email=validated_data.get('Patients')
        AssignedToDoctor=validated_data.get('AssignedToDoctor')
        Appointment=validated_data.get('Appointment')
        selected_item = CounselorAppointment.objects.filter(Patients__email=Patient_email)
        if selected_item.first().Counselor is None:
            selected_item.update(
                Appointment=Appointment,
                Counselor_id=counselor.first().id
            )
            return Response({"Detail":f"new appointment with {Patient_email}"},status=status.HTTP_200_OK)

        if selected_item.first().Counselor.email==Counselor_email:
            selected_item.update(
                Appointment=Appointment,
            )
            return Response({"Detail":f"Your Appointment with {Patient_email} updated"},status=status.HTTP_200_OK)

        else:
            return Response({"Detail":f"Patient {Patient_email} already has an appointment with {selected_item.first().Counselor.email}"},status=status.HTTP_200_OK)