from django.db import models
from Account.models import CustomUser
# Create your models here.
class CounselorAppointment(models.Model):
    Counselor=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='Counselor')
    Patients=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='Patients')
    Appointment=models.DateTimeField(null=True,blank=True)
