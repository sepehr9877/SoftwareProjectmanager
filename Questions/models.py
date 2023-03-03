from django.db import models
from Account.models import CustomUser
# Create your models here.
class SelfAssessment(models.Model):
    Patient=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    Question1=models.CharField(null=False,max_length=50)
    Question2=models.CharField(null=False,max_length=50)
    Question3=models.CharField(null=False,max_length=50)
    Question4 = models.CharField(null=False,max_length=50)
    Question5 = models.CharField(null=False,max_length=50)
    Question6 = models.CharField(null=False,max_length=50)
    Question7 = models.CharField(null=False,max_length=50)
    Question8=models.CharField(null=False,max_length=50)
    Question9=models.CharField(null=False,max_length=50)
    def __str__(self):
        return self.Patient.email