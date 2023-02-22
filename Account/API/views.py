from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView,ListCreateAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,UpdateModelMixin,DestroyModelMixin,RetrieveModelMixin
from rest_framework.response import Response
from Account.models import CustomUser
from .permission import RolePermission, GetAllPatientsPermission
from .serializer import RegistrationSeralizer, UpdateSerializer


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
    lookup_field = 'id'
    permission_classes = (RolePermission,)
    authentication_classes = []
    selected_auth_user=None
    selectedtoken=None
    auth_roles=['doctor','counselor','manager']
    selected_user_by_id=None
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        id = self.kwargs['id']
        selected_token = request.headers['Authorization'].split(' ')[1]
        selectedtoken = Token.objects.filter(key=selected_token).first()
        selected_auth_user = CustomUser.objects.filter(id=selectedtoken.user.id)
        self.selected_user_by_id=CustomUser.objects.filter(id=id)
        if selected_auth_user.first():
            self.selectedtoken=selectedtoken
            self.selected_auth_user = selected_auth_user
            self.request.user=self.selected_auth_user.first()

    def get_serializer_context(self):
        context=super().get_serializer_context()
        id=self.kwargs['id']
        selected_user=CustomUser.objects.filter(id=id).first()
        context['user']=selected_user
        return context
    def get_queryset(self):
        if self.selected_user_by_id.first() is None:return None
        if self.selected_auth_user.first().role=="patient":
            self.check_object_permissions(request=self.request,obj=self.selected_user_by_id.first())
            return self.selected_user_by_id
        if self.selected_auth_user.first().role in self.auth_roles:
            return self.selected_user_by_id
        else:
            return None
    def put(self,request,*args,**kwargs):
        self.check_object_permissions(request=self.request, obj=self.selected_user_by_id.first())
        data=self.request.data
        serializer=UpdateSerializer(data=data)
        if serializer.is_valid():
            updated_user=serializer.update(validated_data=self.request.data,user=self.selected_user_by_id.first())
            return Response({
                            "id":updated_user.id,
                             "first_name":updated_user.first_name,
                            "username":updated_user.username,
                             "last_name":updated_user.last_name,
                            "phonenumber":updated_user.phonenumber,
                            "address":updated_user.address,
                            "birth":updated_user.birth,
                            "email":updated_user.email,
            },status=status.HTTP_200_OK
            )
        else:
            return Response({"Error":serializer.errors})
    def delete(self,request,*args,**kwargs):
        self.check_object_permissions(request=self.request,obj=self.selected_user_by_id.first())
        id=self.selected_user_by_id.first().id
        CustomUser.objects.filter(id=id).delete()
        return Response({"DELETE USER":"SUCCESS","id":id},status=status.HTTP_200_OK)


class CounselorPatientsApi(ListAPIView):
    serializer_class = UpdateSerializer
    permission_classes = [GetAllPatientsPermission,]
    selected_user=None
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        token=self.request.headers['Authorization'].split(' ')[1]
        selected_toke=Token.objects.filter(key__exact=token).first()
        self.selected_user=CustomUser.objects.filter(id=selected_toke.user.id).first()
        self.request.user = self.selected_user
        self.check_permissions(request=self.request)
    def get_queryset(self):
        all_patients=None
        email=self.request.data['email']
        if email:
            all_patients=CustomUser.objects.filter(email=email)
        data=self.request.data
        if data is None:
            all_patients=CustomUser.objects.all()
        return all_patients

