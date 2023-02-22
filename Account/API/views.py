from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView,ListCreateAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,UpdateModelMixin,DestroyModelMixin,RetrieveModelMixin
from rest_framework.response import Response

from Account.models import CustomUser
from .permission import RolePermission
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
                             "Token":token},status=status.HTTP_200_OK)
        else:
            return Response({"Error": serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Create your views here.
class UpdateUserApi(ListAPIView
                    ):
    serializer_class = UpdateSerializer
    lookup_field = 'id'
    permission_classes = (RolePermission,)
    selected_user=None
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        id = self.kwargs['id']
        selected_user = CustomUser.objects.filter(id=id)
        self.selected_user = selected_user
    def get_serializer_context(self):
        context=super().get_serializer_context()
        id=self.kwargs['id']
        selected_user=CustomUser.objects.filter(id=id).first()
        context['user']=selected_user
        return context
    def get_queryset(self):
        self.check_object_permissions(request=self.request,obj=self.selected_user.first())
        selected_user=self.selected_user
        return selected_user
    def put(self,request,*args,**kwargs):
        data=self.request.data
        serializer=UpdateSerializer(data=data)
        if serializer.is_valid():
            updated_user=serializer.update(validated_data=self.request.data,user=self.selected_user.first())
            return Response({"Success":"User Updated"})
        else:
            return Response({"Error":serializer.errors})