from django.db import models
from Account.models import CustomUser
# Create your models here.
class CounselorAppointment(models.Model):
    Counselor=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='Counselor',null=True,blank=True)
    Patient=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='Patients',null=True,blank=True)
    Appointment=models.DateTimeField(null=True,blank=True)
    Status=models.BooleanField(null=True,blank=True)
    Description=models.CharField(max_length=100,null=True,blank=True)

