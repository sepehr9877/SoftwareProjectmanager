from django.db import models
from Account.models import CustomUser
# Create your models here.
from django import forms
class CounselorAppointment(models.Model):
    Counselor=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='Counselor',null=True,blank=True)
    Patient=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='Patients',null=True,blank=True)
    Appointment=models.DateTimeField(null=True,blank=True)
    Accept=models.BooleanField(default=True)
    Description=models.CharField(max_length=100,null=True,blank=True)
    AssigntoDoctor=models.BooleanField(default=False)


class ModelFormCounselorAppointment(forms.ModelForm):
    class Meta:
        models=CounselorAppointment
        fields='__all__'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['Patient'].queryset=CustomUser.objects.filter(role__exact='patient')
        self.fields['Counselor'].queryset=CustomUser.objects.filter(role__exact='counselor')