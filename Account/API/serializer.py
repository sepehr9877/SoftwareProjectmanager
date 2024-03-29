from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer,ModelSerializer,CharField,EmailField,DateField,BooleanField
from Account.models import CustomUser
class RegistrationSeralizer(Serializer):
    firstname=CharField(max_length=50,required=True)
    lastname=CharField(max_length=50,required=True)
    phonenumber=CharField(max_length=50,required=True)
    role=CharField(max_length=50,required=True)
    password=CharField(max_length=50,required=True)
    repassword=CharField(max_length=50,required=True)
    email=EmailField(max_length=50,required=True)
    birth=DateField(required=False)
    rigrationumber=CharField(required=False)
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error=False
    def validate(self,data):
        choice=['patient','doctor','manager','counselor']
        roles=data.get('role')
        if not ( roles in choice):
            self.error = True
            raise ValidationError({"Error": f"the choices are only{choice}"})
        password=data.get('password')
        repassword=data.get('repassword')
        if password!=repassword:
            self.error = True
            raise  ValidationError({"Error":"Passwords Conflict"})
        email=data.get('email')
        selected_email=CustomUser.objects.filter(email=email).first()
        if selected_email:
            self.error = True
            raise ValidationError({"Error": "Email Already Exists"})
        return password,email
    def create(self, validated_data):
        firstname=validated_data.get('firstname')
        lastname=validated_data.get('lastname')
        address=validated_data.get('address')
        email=validated_data.get('email')
        role=validated_data.get('role')
        phone=validated_data.get('phonenumber')
        birth=validated_data.get('birth')
        password=validated_data.get('password')
        CustomUser.objects.create_user(
            email=email,password=password,first_name=firstname,username=firstname,
            last_name=lastname,
            birth=birth,
            role=role,
            phonenumber=phone,
            address=address
        )
        if role =="patient":
            CustomUser.objects.filter(email__exact=email).update(accept=True,description="system accepted you")
        return email,password


class UpdateSerializer(Serializer):
    id=CharField(read_only=True)
    first_name = CharField(max_length=50, required=True)
    last_name = CharField(max_length=50, required=True)
    phonenumber = CharField(max_length=50, required=True)
    birth = DateField(required=True)
    username=CharField(max_length=50,required=True)
    address=CharField(max_length=50,required=True)
    rigrationumber=CharField(required=False)
    role=CharField(read_only=True)
    email=EmailField(read_only=True)
    assessment=BooleanField(read_only=True)
    accept=BooleanField(read_only=True)
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
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error=False
    def validate(self,data):
        password=data.get('password')
        repassword=data.get('repassword')
        email=data.get('email')
        if password!=repassword:
            self.error=True
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
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error=False
    def validate(self,data):
        password=data.get('password')
        email=data.get('email')
        selected_user=CustomUser.objects.filter(email__exact=email).first()
        if selected_user:
            return True
        self.error=True
        raise ValidationError({"Error":"Email is Wrong"})
    def get_value(self, dictionary):
        password=dictionary.get('password')
        email=dictionary.get('email')
        return email,password

