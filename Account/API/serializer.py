from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer,ModelSerializer,CharField,EmailField,DateField
from Account.models import CustomUser
class RegistrationSeralizer(Serializer):
    firstname=CharField(max_length=50,required=True)
    lastname=CharField(max_length=50,required=True)
    phonenumber=CharField(max_length=50,required=True)
    roles=CharField(max_length=50,required=True)
    password=CharField(max_length=50,required=True)
    repassword=CharField(max_length=50,required=True)
    email=EmailField(max_length=50,required=True)
    birth=DateField(required=False)
    rigrationumber=CharField(required=False)

    def validate(self,data):
        password=data.get('password')
        repassword=data.get('repassword')
        if password!=repassword:
            raise ValidationError({"Error":"Passwords Confilict"})
        email=data.get('email')
        selected_email=CustomUser.objects.filter(email=email).first()
        if selected_email:
            raise ValidationError({"Error": "Email Already Exists"})
        return password,email
    def create(self, validated_data):
        firstname=validated_data.get('firstname')
        lastname=validated_data.get('lastname')
        email=validated_data.get('email')
        role=validated_data.get('roles')
        phone=validated_data.get('phone')
        birth=validated_data.get('birth')
        password=validated_data.get('password')
        CustomUser.objects.create_user(
            email=email,password=password,first_name=firstname,username=firstname,
            last_name=lastname,
            birth=birth,
            role=role,
            phonenumber=phone,
        )
        return email,password
