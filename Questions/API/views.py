from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from Account.models import CustomUser
from .permissions import CheckPermissionSelfAssessment
from .serializer import SelfAssessMentSerializer
from ..models import SelfAssessment


class SelfAssessmentApi(ListAPIView):
    serializer_class = SelfAssessMentSerializer
    permission_classes = [CheckPermissionSelfAssessment,]
    patient=None
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        auth_token=self.request.headers['Authorization'].split(' ')[1]
        selected_token=Token.objects.filter(key__exact=auth_token).first()
        if selected_token:
            self.patient=CustomUser.objects.filter(id=selected_token.user.id)
            self.request.user=self.patient.first()
        self.check_permissions(request=self.request)
    def get_queryset(self):
        selected_question=SelfAssessment.objects.filter(Patient_id=self.patient.first().id)
        return selected_question
    def post(self, request, *args, **kwargs):
        data=self.request.data

        serializer=SelfAssessMentSerializer(data=data)
        serializer.context['patient']=self.patient
        selected_selfAssessment=SelfAssessment.objects.filter(Patient_id=self.patient.first().id)
        if selected_selfAssessment:
            return Response({"Success":"Form is already Complete",
                             "Status":"Pending",
                             "Description":"you have already completed the form , wait for counselor"},status=status.HTTP_200_OK)

        if serializer.is_valid():

            serializer.create(validated_data=data)
            return Response({"Success":"Form is Complete",
                             "Status":"Pending",
                             "Description":"Wait for Counselor to make you an appointment ,or assign to a doctor"},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
