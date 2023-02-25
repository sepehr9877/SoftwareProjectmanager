from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
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


class UpdateSerializer(Serializer):
    id=CharField(read_only=True)
    first_name = CharField(max_length=50, required=True)
    last_name = CharField(max_length=50, required=True)
    phonenumber = CharField(max_length=50, required=True)
    email = EmailField(max_length=50, required=True)
    birth = DateField(required=True)
    username=CharField(max_length=50,required=True)
    address=CharField(max_length=50,required=True)
    rigrationumber=CharField(required=False)
    role=CharField(read_only=True)

    # def get_initial(self):
    #     initial = None
    #     if self.context is not None:
    #         select_user=self.context['user']
    #         if select_user:
    #             initial={
    #                 "first_name":select_user.first_name,
    #                 "username":select_user.username,
    #                 "last_name":select_user.last_name,
    #                 "email":select_user.email,
    #                 "phonenumber":select_user.phonenumber,
    #                 "birth":select_user.birth,
    #                 "address":select_user.address,
    #             }
    #     return initial

    def update(self,validated_data,user):
        firstname=validated_data["first_name"]
        lastname=validated_data["last_name"]
        username=validated_data["username"]
        phonumber=validated_data["phonenumber"]
        birth=validated_data["birth"]
        address=validated_data["address"]
        id=user.id
        update_user=CustomUser.objects.filter(id=id).update(
            first_name=firstname,
            last_name=lastname,
            address=address,
            phonenumber=phonumber,
            birth=birth,
            username=username
        )
        selected_updated_user=CustomUser.objects.filter(id=id).first()
        return selected_updated_user

class PasswordEmail(Serializer):
    email=CharField(max_length=50)
    password=CharField(max_length=50)
    repassword=CharField(max_length=50)
    def validate(self,data):
        password=data.get('password')
        repassword=data.get('repassword')
        email=data.get('email')
        if password!=repassword:
            raise ValidationError({"Error":"Check your password"})
        return True
    def update(self,validated_data,user):
        email=validated_data.get('email')
        password=validated_data.get('password')
        password_crypted=make_password(password=password)
        user.update(
            email=email,password=password_crypted
        )
        return True
class LoginSerializer(Serializer):
    email=CharField(max_length=50,required=True)
    password=CharField(max_length=50,required=True)

    def validate(self,data):
        password=data.get('password')
        email=data.get('email')
        selected_user=CustomUser.objects.filter(email__exact=email).first()
        if selected_user:
            return True
        raise ValidationError({"Error":"Email is Wrong"})
    def get_value(self, dictionary):
        password=dictionary.get('password')
        email=dictionary.get('email')
        return email,password