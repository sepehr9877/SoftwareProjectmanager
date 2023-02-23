from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView,ListCreateAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,UpdateModelMixin,DestroyModelMixin,RetrieveModelMixin
from rest_framework.response import Response
from Account.models import CustomUser
from .permission import RolePermission, PasswordEmailPermission
from .serializer import RegistrationSeralizer, UpdateSerializer, PasswordEmail


class RegisterApi(ListAPIView):
    serializer_class = RegistrationSeralizer
    def get_queryset(self):None
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
            return Response({"Error": serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Create your views here.
class UpdateUserApi(ListAPIView
                    ):
    serializer_class = UpdateSerializer
    permission_classes = (RolePermission,)
    authentication_classes = []
    selected_auth_user=None
    selectedtoken=None
    auth_roles=['doctor','counselor','manager']
    selected_user_by_email=None
    lookup_url_kwarg = 'email'
    selected_roles=None
    selected_by_roles=None
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        selected_token = request.headers['Authorization'].split(' ')[1]
        selectedtoken = Token.objects.filter(key=selected_token).first()
        selected_auth_user=None
        if selectedtoken.first():
            selected_auth_user = CustomUser.objects.filter(id=selectedtoken.user.id)
            self.selectedtoken=selectedtoken
            self.selected_auth_user = selected_auth_user
            self.request.user=self.selected_auth_user.first()
        email = self.request.GET.get('email')
        roles = self.request.GET.get('role')
        if email:
            self.selected_user_by_email = CustomUser.objects.filter(email=email)
        if selected_auth_user.first().role in self.auth_roles:
            if roles and email:
                self.selected_user_by_email = CustomUser.objects.filter(role=roles,email=email)
            elif roles:
                self.selected_by_roles = CustomUser.objects.filter(role=roles).all()

        else:
            self.check_object_permissions(request=self.request, obj=self.selected_user_by_email)

    def get_serializer_context(self):
        context=super().get_serializer_context()
        email = self.request.GET.get('email')
        if email:
            selected_user=CustomUser.objects.filter(email=email).first()
            context['user']=selected_user
        return context
    def get_queryset(self):
        if self.selected_user_by_email:
            return self.selected_user_by_email
        if self.selected_by_roles:
            return self.selected_by_roles
        else:
            return None
    def put(self,request,*args,**kwargs):
        data=self.request.data
        serializer=UpdateSerializer(data=data)
        if serializer.is_valid():
            updated_user=serializer.update(validated_data=self.request.data, user=self.selected_user_by_email.first())
            return Response({
                            "id":updated_user.id,
                             "first_name":updated_user.first_name,
                            "username":updated_user.username,
                             "last_name":updated_user.last_name,
                            "phonenumber":updated_user.phonenumber,
                            "address":updated_user.address,
                            "birth":updated_user.birth,
                            "email":updated_user.email,
                            "role":updated_user.role
            },status=status.HTTP_200_OK
            )
        else:
            return Response({"Error":serializer.errors})
    def delete(self,request,*args,**kwargs):
        id=self.selected_user_by_email.first().id
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

    def get_queryset(self):return None
    def put(self,request,*args,**kwargs):
        serilaizer=PasswordEmail(data=self.request.data)
        if serilaizer.is_valid():
            email=self.request.data.get('email')
            user_emal=self.authuser.first().email
            if email!=user_emal:
                serilaizer.update(self.request.data,self.authuser)
            return Response({"Success":"User Updated","email":self.authuser.first().email})
        else:
            return Response({"Error":serilaizer.errors},status=status.HTTP_400_BAD_REQUEST)
