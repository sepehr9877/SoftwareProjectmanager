from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError, MethodNotAllowed
from rest_framework.generics import ListAPIView,ListCreateAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,UpdateModelMixin,DestroyModelMixin,RetrieveModelMixin
from rest_framework.response import Response
from Account.models import CustomUser
from Questions.models import SelfAssessment
from .permission import RolePermission, PasswordEmailPermission
from .serializer import RegistrationSeralizer, UpdateSerializer, PasswordEmail, LoginSerializer
import json
class RegisterApi(ListAPIView):
    serializer_class = RegistrationSeralizer
    def get_queryset(self):return None
    def post(self,request,*args,**kwargs):
        data=self.request.data
        serializer=RegistrationSeralizer(data=data)
        if serializer.is_valid():
            email,password=serializer.create(validated_data=data)
            auth=authenticate(self.request,email=email,password=password)
            selected_user=CustomUser.objects.filter(email=email).first()
            token=Token.objects.create(user_id=selected_user.id)
            login(request=self.request,user=auth)
            return Response({"Success":"User Register",
                             "Token":token.key},status=status.HTTP_200_OK)
        else:
            error = json.dumps(serializer.errors)
            err = json.loads(error)
            send_error = None
            if getattr(serializer, 'error'):
                json_error = err["Error"][0]
                send_error = {"Error": json_error}
            else:
                send_error = serializer.errors
            return Response(send_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Create your views here.
class UpdateUserApi(ListAPIView
                    ):
    serializer_class = UpdateSerializer
    permission_classes = (RolePermission,)
    selected_auth_user=None
    selectedtoken=None
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        selected_token = request.headers['Authorization'].split(' ')[1]
        selectedtoken = Token.objects.filter(key=selected_token).first()
        selected_auth_user=None
        if selectedtoken:
            selected_auth_user = CustomUser.objects.filter(id=selectedtoken.user.id)
            self.selectedtoken=selectedtoken
            self.selected_auth_user = selected_auth_user
            self.request.user=self.selected_auth_user.first()

        self.check_permissions(request=self.request)

    def get_queryset(self):
        raise MethodNotAllowed(self.request.method)
    def put(self,request,*args,**kwargs):
        data=self.request.data
        serializer=UpdateSerializer(data=data)
        if serializer.is_valid():
            updated_user=serializer.update(validated_data=self.request.data, user=self.selected_auth_user.first())
            return Response({
                            "id":updated_user.id,
                             "first_name":updated_user.first_name,
                            "username":updated_user.username,
                             "last_name":updated_user.last_name,
                            "phonenumber":updated_user.phonenumber,
                            "address":updated_user.address,
                            "birth":updated_user.birth,
                            "email":updated_user.email,
                            "role":updated_user.role,
                            "assessment":updated_user.assessment
            },status=status.HTTP_200_OK
            )
        else:
            error = json.dumps(serializer.errors)
            err = json.loads(error)
            send_error = None
            if getattr(serializer, 'error'):
                json_error = err["Error"][0]
                send_error = {"Error": json_error}
            else:
                send_error = serializer.errors
            return Response(send_error,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,*args,**kwargs):
        id=self.selected_auth_user.first().id
        CustomUser.objects.filter(id=id).delete()
        return Response({"DELETE USER":"SUCCESS","id":id},status=status.HTTP_200_OK)



class UpdatePasswordEmailApi(ListAPIView):
    serializer_class = PasswordEmail
    permission_classes = [PasswordEmailPermission,]
    authuser=None
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        token=self.request.headers['Authorization'].split(' ')[1]
        selected_token=Token.objects.filter(key__exact=token).first()
        if selected_token:
            self.authuser=CustomUser.objects.filter(id=selected_token.user.id)
            self.request.user=self.authuser
        self.check_permissions(self.request)

    def get_queryset(self):raise MethodNotAllowed(self.request.method)
    def put(self,request,*args,**kwargs):
        serilaizer=PasswordEmail(data=self.request.data)
        if serilaizer.is_valid():
            email=self.request.data.get('email')
            user_emal=self.authuser.first().email
            if email!=user_emal:
                serilaizer.update(self.request.data,self.authuser)
            return Response({"Success":"User Updated","email":self.authuser.first().email})
        else:
            error = json.dumps(serilaizer.errors)
            err = json.loads(error)
            send_error = None
            if getattr(serilaizer, 'error'):
                json_error = err["Error"][0]
                send_error = {"Error": json_error}
            else:
                send_error = serilaizer.errors
            return Response(send_error,status=status.HTTP_400_BAD_REQUEST)
class LoginApi(ListAPIView):
    serializer_class = LoginSerializer
    allow_method=['POST']
    def get_queryset(self):raise MethodNotAllowed(self.request.method)
    def post(self,request,*args,**kwargs):
        data=self.request.data
        serialzier=LoginSerializer(data=data)
        if serialzier.is_valid():
            email,password=serialzier.get_value(dictionary=data)
            auth_user=authenticate(self.request,email=email,password=password)
            if auth_user:
                selected_user=CustomUser.objects.filter(email__exact=email).first()
                selected_token=Token.objects.filter(user_id=selected_user.id).first()
                self_assessment=SelfAssessment.objects.filter(Patient_id=selected_user.id)
                assessment=False
                if(self_assessment):
                    assessment=True
                return Response({"Status":"Login Successfully",
                                 "User":selected_user.email,
                                 "role":selected_user.role,
                                 "Token":selected_token.key,
                                 "assessment":assessment},status=status.HTTP_200_OK)
            else:
                return Response({"Error":"Invalid Password"},status=status.HTTP_400_BAD_REQUEST)
        else:
            error = json.dumps(serialzier.errors)
            err = json.loads(error)
            send_error = None
            if getattr(serialzier,'error'):
                json_error = err["Error"][0]
                send_error = {"Error": json_error}
            else:
                send_error = serialzier.errors
            return Response(send_error,status=status.HTTP_400_BAD_REQUEST)

class GetAllDetail(ListAPIView):
    serializer_class = UpdateSerializer
    authuser=None
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        token=self.request.headers['Authorization'].split(' ')[1]
        selected_user=Token.objects.filter(key__exact=token)
        self.authuser=CustomUser.objects.filter(id=selected_user.first().user.id)

    def get_queryset(self):
        if self.authuser is None:
            return Response({"Error":"Please set Token into Header"},status=status.HTTP_400_BAD_REQUEST)
        return self.authuser
