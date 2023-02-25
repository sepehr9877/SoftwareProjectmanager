from django.db import models
from Account.models import CustomUser
# Create your models here.
class CounselorAppointment(models.Model):
    Counselor=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='Counselor',null=True,blank=True)
    Patients=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='Patients',null=True,blank=True)
    Appointment=models.DateTimeField(null=True,blank=True)
