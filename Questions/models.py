from django.db import models
from Account.models import CustomUser
# Create your models here.
class SelfAssessment(models.Model):
    Patient=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    Question1=models.BooleanField(null=False)
    Question2=models.BooleanField(null=False)
    Question3=models.BooleanField(null=False)
    Question4 = models.BooleanField(null=False)
    Question5 = models.BooleanField(null=False)
    Question6 = models.BooleanField(null=False)
    Question7 = models.BooleanField(null=False)
    Question8=models.BooleanField(null=False)
    Question9=models.BooleanField(null=False,default=False)
    def __str__(self):
        return self.Patient.email