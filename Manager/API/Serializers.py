from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.serializers import Serializer,EmailField,BooleanField,CharField,DateTimeField

from Account.models import CustomUser


class AcceptRejectDoctorSerializer(Serializer):
    first_name = CharField(read_only=True)
    last_name = CharField(read_only=True)
    email=EmailField(required=True)
    accept=BooleanField(required=True)
    description=CharField(required=True)
    def validate(self, data):
        email=data.get('email')
        role=['doctor']
        user=CustomUser.objects.filter(email__exact=email)
        if user.first() is None :
            self.error=True
            raise ValidationError({"Error":"you need to insert a valid email"})
        if not user.first().role in role:
            self.error=True
            raise ValidationError({"Error":"you have to set doctor email address"})
        return data
    def update(self, manager, validated_data):
        email=validated_data.get('email')
        accept=validated_data.get('accept')
        description=validated_data.get('description')
        CustomUser.objects.filter(email__exact=email).update(
            accept=accept,description=description
        )
        customer =CustomUser.objects.filter(email__exact=email).first()
        return Response({"email":customer.email,
                         "accept":customer.accept,
                         "description":customer.description})


class AcceptRejectCounselorSerializer(Serializer):
    first_name = CharField(read_only=True)
    last_name = CharField(read_only=True)
    email=EmailField(required=True)
    accept=BooleanField(required=True)
    description=CharField(required=True)
    def validate(self, data):
        email=data.get('email')
        role=['counselor']
        user=CustomUser.objects.filter(email__exact=email)
        if user.first() is None :
            self.error=True
            raise ValidationError({"Error":"you need to insert a valid email"})
        if not user.first().role in role:
            self.error=True
            raise ValidationError({"Error":"you have to set counselor email address"})
        return data
    def update(self, manager, validated_data):
        email=validated_data.get('email')
        accept=validated_data.get('accept')
        description=validated_data.get('description')
        CustomUser.objects.filter(email__exact=email).update(
            accept=accept,description=description
        )
        customer =CustomUser.objects.filter(email__exact=email).first()
        return Response({"email":customer.email,
                         "accept":customer.accept,
                         "description":customer.description})
class ManagerDateDocotorPatientSerializer(Serializer):
    Patient = EmailField(read_only=True)
    Doctor = EmailField(read_only=True)
    Appointment = DateTimeField(read_only=True)
    Accept = BooleanField(read_only=True)
    Description =CharField(read_only=True)

class AcceptRejectPatientSerializer(Serializer):
    first_name=CharField(read_only=True)
    last_name=CharField(read_only=True)
    email=EmailField(required=True)
    accept=BooleanField(required=True)
    description=CharField(required=True)

    def validate(self, data):
        email=data.get('email')
        role=['patient']
        user=CustomUser.objects.filter(email__exact=email)
        if user.first() is None :
            self.error=True
            raise ValidationError({"Error":"you need to insert a valid email"})
        if not user.first().role in role:
            self.error=True
            raise ValidationError({"Error":"you have to set patient email address"})
        return data
    def update(self, manager, validated_data):
        email=validated_data.get('email')
        accept=validated_data.get('accept')
        description=validated_data.get('description')
        CustomUser.objects.filter(email__exact=email).update(
            accept=accept,description=description
        )
        customer =CustomUser.objects.filter(email__exact=email).first()
        return Response({"email":customer.email,
                         "accept":customer.accept,
                         "description":customer.description})


class MangerDateCounselorPatientSerilizer(Serializer):
        Counselor = EmailField(read_only=True)
        Patient =EmailField(read_only=True)
        Appointment = DateTimeField(read_only=True)
        Accept = BooleanField(read_only=True)
        Description =CharField(read_only=True)
        AssigntoDoctor =BooleanField(read_only=True)
        Doctor = CharField(read_only=True)


