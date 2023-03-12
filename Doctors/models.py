
from django.db import models
from django import forms

from Account.models import CustomUser
# Create your models here.
class DoctorAppointment(models.Model):
    Patient=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="Patient",null=True,blank=True)
    Doctor=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="Doctor",null=True,blank=True)
    Appointment=models.DateTimeField(null=True,blank=True)
    Accept=models.BooleanField(default=True)
    Description=models.CharField(max_length=100,null=True,blank=True)

class ModelFormDoctorAppointment(forms.ModelForm):
    class Meta:
        models=DoctorAppointment
        fields='__all__'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['Patient'].queryset=CustomUser.objects.filter(role__exact='patient')
        self.fields['Doctor'].queryset=CustomUser.objects.filter(role__exact='doctor')

