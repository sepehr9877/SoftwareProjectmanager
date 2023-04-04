from rest_framework.serializers import Serializer,CharField,EmailField,BooleanField,DateTimeField


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

